/* Project specific Javascript goes here. */
jQuery(document).ready(function($){
   $('.municipality_list').find('li:first').addClass('active');
   $('#id_location_and_scope_form-location-district').change(function(event){
        var _this=$(this);
        var district = _this.val();
        $('.municipality_list').find('li.active').removeClass('active').find('input:checked').removeAttr('checked');
        $('[data-district-id="'+ district +'"]').addClass('active');
   });
   $('.add-scope-field').click(function(event){
       var _this = $(this);
       var parents = _this.parents('.row-fluid:first');
       var clone = parents.prev('.row-fluid').clone(true);
       clone.find('input, select').each(function(){
           var _this = $(this);
           var attr = ['id', 'name'];
           $.each(attr, function(i,v){
               var old_attr = _this.attr(v);
               _this.attr(v,old_attr.replace(/\d+/,parseInt(old_attr.match(/\d+/g))+1))
           });
       });
       var tf_field = $('#id_location_and_scope_form-scope-TOTAL_FORMS');
       var total_forms = tf_field.val();
       tf_field.val(parseInt(total_forms)+1);
       parents.before(clone);
   });
   
   /** Show referenced tab if there is one */
   if(window.location.hash && $('.nav-tabs').length) {
       $('[href="' + window.location.hash + '"]').tab('show');
   }
});