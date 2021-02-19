function LoadDropdown () {
  let styles_container = document.getElementById('id_style_container');
  let list_menu = document.getElementById('id_list_menu');
  let all_field_type_list = document.querySelectorAll("input.field-type[value='list']");

  // On vérifie si il existe des champs de type 'list' et on affiche ou cache le conteneur
  let all_field_type_list_values = Array.from(all_field_type_list).map(el => el.value);
  if (!all_field_type_list_values.find(el => el === 'list')) {
    styles_container.style.display = 'none';
  } else {
    styles_container.style.display = '';
  }

  for (const field_type of all_field_type_list) {
    // si l'identifiant du champs n'est pas déjà
    // dans la dropdown on l'ajoute
    let list_id = field_type.id
    let already_exists = document.getElementById(list_id+"_styles")

    if (!already_exists) {
      let id_label = list_id.replace('field_type', 'label');
      let id_name = list_id.replace('field_type', 'name');
      let list_label = document.getElementById(id_label)
      let list_name = document.getElementById(id_name)

      let item = document.createElement("div");
      item.id = list_id + '_styles';
      item.className = "item";
      item.setAttribute("data-value", list_name.value);
      item.innerHTML = list_label.value;
      list_menu.appendChild(item);
    }
  }

  // On enlève les veleurs qui n'existent plus
  const all_field_type_list_arr = Array.from(all_field_type_list);
  const all_field_type_ids = all_field_type_list_arr.map(el => el.id);
  for (const item of Array.from(list_menu.getElementsByClassName('item'))) {
    const value = item.id.replace('_styles', '');
    if (!all_field_type_ids.find(el => el === value)) {
      list_menu.removeChild(item)
    }
  }
}

function displayColorSelection() {
  if (this.value) {
    let colors_selection_container = document.getElementById('id_colors_selection');
    colors_selection_container.hidden = false;
    colors_selection_container.innerHTML = '';

    let selection = document.getElementById('id_list_selection').querySelector(`[data-value=${this.value}]`);
    let id_options = selection.id.replace('field_type_styles', 'options');
    let options = document.getElementById(id_options).value.split(',');
    for (let option of options) {
      const colorDiv = document.createElement('div');
      colorDiv.classList.add('color-input')
      const colorLabel = document.createElement('label');
      colorLabel.innerHTML = option;
      const colorInput = document.createElement('input');
      colorInput.type = 'color';
      colorDiv.appendChild(colorLabel);
      colorDiv.appendChild(colorInput);
      colors_selection_container.appendChild(colorDiv);
    }
  }
}

window.addEventListener('load', function () {
  LoadDropdown();

  // On parcoure les formets de champs personnalisé
  let personnalizedFields = document.getElementsByClassName('pers-field');
  // Dans chaque formset, on récupère l'input du dropdown 'Type de champ'
  // et on met l'event dessus
  for (let field of personnalizedFields) {
    let listDropdown = field.getElementsByClassName('ui selection dropdown')[0].getElementsByTagName('input')[0];
    listDropdown.addEventListener('change', LoadDropdown, false);
  }

  let field_type_selection = document.getElementById('id_list_selection').getElementsByTagName('input')[0];
  field_type_selection.addEventListener('change', displayColorSelection, false);
});
