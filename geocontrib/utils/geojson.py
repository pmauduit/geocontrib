from uuid import uuid4
import json
import logging

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos.error import GEOSException
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from geocontrib.models import Feature
from geocontrib.models import FeatureLink

logger = logging.getLogger(__name__)

class GeoJSONProcessingFailed(Exception):
    pass


class GeoJSONProcessing:

    def __init__(self, *args, **kwargs):
        self.infos = []

    def get_geom(self, geom):
        # Si geoJSON
        if isinstance(geom, dict):
            geom = str(geom)
        try:
            geom = GEOSGeometry(geom, srid=4326)
        except (GEOSException, ValueError):
            geom = None
        return geom

    def get_feature_data(self, feature_type, properties, field_names):
        feature_data = {}
        if hasattr(feature_type, 'customfield_set'):
            for field in field_names:
                feature_data[field] = properties.get(field)
        return feature_data

    def handle_title(self, title, feature_id):
        if not title or title == '':
            title = feature_id
            if not feature_id or feature_id == '':
                uid = uuid4()
                feature_id = str(uid)
                title = feature_id

        return title, feature_id

    @transaction.atomic
    def create_features(self, data, import_task):
        feature_type = import_task.feature_type
        new_features = data.get('features')
        nb_features = len(new_features)
        field_names = feature_type.customfield_set.values_list('name', flat=True)

        for feature in new_features:
            properties = feature.get('properties')

            feature_data = self.get_feature_data(
                feature_type, properties, field_names)

            title, feature_id = self.handle_title(
                properties.get("title"), feature.get("id"))

            description = properties.get('description')

            status = properties.get('status', 'draft')
            if status not in [choice[0] for choice in Feature.STATUS_CHOICES]:
                logger.warn("Feature '%s' import: status '%s' unknown, defaulting to 'draft'",
                            title, status)
                status = "draft"

            try:
                try:
                    feature_exist = Feature.objects.get(feature_id=feature_id)
                except Feature.DoesNotExist:
                    feature_exist = None
                    # Le geojson peut venir avec un ancien ID. On reset l'ID ici aussi
                    feature_id = None
               
                if feature_exist:
                    if feature_exist.project != feature_type.project or feature_exist.feature_type != feature_type:
                        # Si l'ID qui vient du geojson de l'import existe, 
                        # mais on souhaite créer le signalement dans un autre projet
                        # On set l'ID à None
                        feature_id = None
                current, _ = Feature.objects.update_or_create(
                    feature_id=feature_id,
                    # project=feature_type.project,
                    defaults={
                        'title': title,
                        'description' : description,
                        # TODO fix status
                        'status': status,
                        'creator': import_task.user,
                        'project' : feature_type.project,
                        'feature_type' : feature_type,
                        'geom' : self.get_geom(feature.get('geometry')),
                        'feature_data' : feature_data,
                    }
                )
                
            except Exception as er:
                logger.exception(
                    f"L'edition de feature a echoué {er}'. ")
                self.infos.append(
                    f"L'edition de feature a echoué {er}'. ")
                raise GeoJSONProcessingFailed

            if title:
                simili_features = Feature.objects.filter(
                    Q(title=title, description=description, feature_type=feature_type) | Q(
                        geom=current.geom, feature_type=feature_type)
                ).exclude(feature_id=current.feature_id)
                if simili_features.exists():
                    for row in simili_features:
                        FeatureLink.objects.get_or_create(
                            relation_type='doublon',
                            feature_from=current,
                            feature_to=row
                        )
        if nb_features > 0:
            msg = "{nb} signalement(s) importé(s). ".format(nb=nb_features)
            self.infos.append(msg)

    def check_feature_type(self, data, import_task):
        feature_type = import_task.feature_type

        features = data.get('features', [])
        if len(features) == 0:
            self.infos.append(
                "Aucun signalement n'est indiqué dans l'entrée 'features'. ")
            raise GeoJSONProcessingFailed

        for feature in features:
            geom = feature.get('geometry')
            if str(geom['type']).lower() != feature_type.geom_type:
                self.infos.append(
                    f"L'edition de feature a echoué. Le type de features sont différents. ")
                raise GeoJSONProcessingFailed

    # # FUNCTION DEACTIVATE 
    # def check_feature_type_slug(self, data, import_task):
    #     feature_type_slug = import_task.feature_type.slug
    #     features = data.get('features', [])
    #     if len(features) == 0:
    #         self.infos.append(
    #             "Aucun signalement n'est indiqué dans l'entrée 'features'. ")
    #         raise GeoJSONProcessingFailed

    #     for feat in features:
    #         feature_type_import = feat.get(
    #             'properties', {}).get('feature_type')

    #         if not feature_type_import:
    #             self.infos.append(
    #                 "Le type de signalement doit etre indiqué dans l'entrée 'feature_type' de chaque signalement. ")
    #             raise GeoJSONProcessingFailed

    #         elif feature_type_import != feature_type_slug:

    #         if feature_type_import != feature_type_slug:
    #             self.infos.append(
    #                 "Le type de signalement ne correspond pas à celui en cours de création: '{dest}'. ".format(
    #                     dest=feature_type_slug
    #                 ))
    #             raise GeoJSONProcessingFailed

    def validate_data(self, file):
        try:
            up_file = file.read()
            data = json.loads(up_file.decode('utf-8'))
        except Exception as err:
            self.infos.append(
                "Erreur à la lecture du fichier GeoJSON: {} ".format(str(err)))
            raise GeoJSONProcessingFailed
        else:
            return data

    def __call__(self, import_task):
        try:
            import_task.status = "processing"
            import_task.started_on = timezone.now()
            data = self.validate_data(import_task.file)
            # self.check_feature_type_slug(data, import_task)
            self.check_feature_type(data, import_task)
            self.create_features(data, import_task)
        except GeoJSONProcessingFailed:
            import_task.status = "failed"
        else:
            import_task.status = "finished"
            import_task.finished_on = timezone.now()
        import_task.infos = "/n".join(self.infos)
        import_task.save(update_fields=['status', 'started_on', 'finished_on', 'infos'])


def geojson_processing(import_task):
    process = GeoJSONProcessing()
    process(import_task)
