document.querySelectorAll('.input-group').forEach(group => {
  if (group.querySelector('input:required')) {
    group.querySelector('label').innerHTML += '<span style="color: red;">*</span>';
  }
});
