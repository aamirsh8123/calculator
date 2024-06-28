$(function () {
  // Cache the jQuery selectors for better performance
  var $additive = $('#id_additive'),
      $liquied_narrow = $('#id_liquied_narrow'),
      $swu = $('#id_swu'),
      $additive_type = $('#id_additive_type'),
      $resin = $('#id_resin'),
      $special_attribute = $('#id_special_attribute'),
      $special_requirement = $('#id_special_requirement'),
      $ink_type = $('#id_ink_type'),
      $color_type = $('#id_color_type'),
      $color_code_choice = $('#id_color_code_choice'),
      $press = $('#id_press'),
      $mg_code = $('#id_mg_code'),
      $ph_code = $('#id_ph_code');

  // Function to handle enabling/disabling fields
  function handleFieldToggle() {
      var additiveVal = $additive.val();
      var enableNextField = function (currentField, nextField) {
          if (currentField.val()) {
              nextField.prop('disabled', false);
          }
      };

      // Enable/disable fields based on 'additive' value
      if (additiveVal === '1') {
          enableNextField($additive, $liquied_narrow);
          enableNextField($liquied_narrow, $swu);
          enableNextField($swu, $additive_type);
      } else if (additiveVal === '2') {
          enableNextField($additive, $liquied_narrow);
          enableNextField($liquied_narrow, $swu);
          enableNextField($swu, $additive_type);
          enableNextField($additive_type, $resin);
      }
  }

  // Attach change event handlers
  $additive.change(handleFieldToggle);
  $liquied_narrow.change(handleFieldToggle);
  $swu.change(handleFieldToggle);
  $additive_type.change(handleFieldToggle);
  $resin.change(function () {
      $special_attribute.prop('disabled', $resin.val() === "");
  });
  $special_attribute.change(function () {
      var specialAttrVal = $special_attribute.val();
      $special_requirement.prop('disabled', specialAttrVal !== '1');
      $ink_type.prop('disabled', specialAttrVal === '1');
  });
  $special_requirement.change(function () {
      $ink_type.prop('disabled', $special_requirement.val() === "");
  });
  $ink_type.change(function () {
      $color_type.prop('disabled', $ink_type.val() === "");
  });
  $color_type.change(function () {
      var colorTypeVal = $color_type.val();
      $color_code_choice.prop('disabled', $special_attribute.val() === '1' || colorTypeVal === "");
      $press.prop('disabled', colorTypeVal === "");
  });

  // Initial field toggle check
  handleFieldToggle();

  // AJAX request when fields change
  $('#id_additive, #id_liquied_narrow, #id_swu, #id_additive_type, #id_resin, #id_special_attribute, #id_special_requirement, #id_ink_type, #id_color_type, #id_color_code_choice, #id_press').change(function () {
    var additiveVal = $additive.val();  
    $.ajax({
          url: getValues, // Ensure getValues is defined and correct
          method: 'GET',
          dataType: 'json',
          data: {
              'additive': additiveVal,
              'liquied_narrow': $liquied_narrow.val(),
              'swu': $swu.val(),
              'additive_type': $additive_type.val(),
              'resin': $resin.val(),
              'special_attribute': $special_attribute.val(),
              'special_requirement': $special_requirement.val(),
              'ink_type': $ink_type.val(),
              'color_type': $color_type.val(),
              'color_code_choice': $color_code_choice.val(),
              'press': $press.val(),
          },
          success: function (data) {
              // Update the respective fields based on the additive value
              $mg_code.val(data.material_group);
              $ph_code.val(additiveVal === '1' ? data.product_hierarchy_a : data.product_hierarchy_b);
          },
          error: function (xhr, status, error) {
              console.error('AJAX error:', status, error);
          }
      });
  });
});
