$(function () {
  $('#id_additive, #id_swu, #id_special_attribute').change(function () {
    var additiveValue = $('#id_additive').val();
    var swuValue = $('#id_swu').val();
    var specialAttributeValue = $('#id_special_attribute').val();
    var color_type = $('#id_color_type').val();
    var changedElementId = $(this).attr('id');


    $.ajax({
      url: populateFields,  // Update this with your actual AJAX URL endpoint
      data: {
        'additive': additiveValue,
        'swu': swuValue,
        'special_attribute': specialAttributeValue,
        'color_type': color_type,
      },
      success: function (data) {
        // Update the choices based on the changed element
        if (changedElementId === 'id_additive') {
          updateChoices('#id_liquied_narrow', data.liquied_narrow);
          updateChoices('#id_swu', data.swu);
          updateChoices('#id_additive_type', data.additive_type);
        } else if (changedElementId === 'id_swu' && additiveValue === '2') {
          updateChoices('#id_additive_type', data.additive_type);
          updateChoices('#id_resin', data.resin);
          updateChoices('#id_special_attribute', data.special_attribute);
          updateChoices('#id_ink_type', data.ink_type);
          updateChoices('#id_color_type', data.color_type);
          updateChoices('#id_press', data.press);
        } else if (changedElementId === 'id_special_attribute') {
          updateChoices('#id_special_requirement', data.special_requirement);
        }
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.error(`AJAX request failed: ${textStatus}, ${errorThrown}`);
      }
    });
  });
});

function updateChoices(selector, choices) {
  var $select = $(selector);
  $select.empty().append($('<option>', { value: '', text: '---------' }));
  choices.forEach(function (choice) {
    $select.append($('<option>', { value: choice.id, text: choice.item_name }));
  });
}

$(function() {
  // Trigger the AJAX call when needed, for example on a dropdown change
  $('#id_color_type').change(function() {
      var selectedInkType = $(this).val(); // Get the selected ink type from your dropdown

      $.ajax({
          url: getColorChoice, // The URL to your Django view
          data: {
              'color_type': selectedInkType // Pass the selected ink type as a GET parameter
          },
          dataType: 'json',
          success: function(data) {
              // Clear the existing options
              $('#id_color_code_choice').empty();
              // Append a null value option
              $('#id_color_code_choice').append($('<option>', { 
                value: '',
                text : '---------' // You can set the placeholder text here
            }));
              // Handle the successful response here
              $.each(data, function(index, item) {
                  // Assuming 'item' is an object with 'id' and 'color_code' properties
                  $('#id_color_code_choice').append($('<option>', { 
                      value: item.id,
                      text : item.color_code 
                  }));
              });
          },
          error: function(xhr, status, error) {
              // Handle any errors here
              console.error(error); // Log the error to the console for debugging
          }
      });
  });
});

