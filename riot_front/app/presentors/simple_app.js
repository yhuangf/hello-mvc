

/* The presenter */

(function() { 'user strict';

  window.simple = new Simple();

  // HTML for single item
  var template = $("[type='html/todo']").html(),
    root = $("#todo-list"),
    nav = $("#filters a")
 
  /* user events */ 


  /* model events */
  
  simple.on("add", add).on("remove", function(items) {
    $.each(items, function() {
      $("#" + this.id).remove()
    })  

  }).on("toggle", function(item) {
    toggle($("#" + item.id), !!item.done)

  }).on("add remove toggle", counts)



  /* Private functions */

  function toggle(el, flag){
    el.toggleClass("completed", flag);
    $(":checkbox", el).prop("checked", flag);
  }

  function add(item) {
    if (this.id) item = this;
    
    // Add the element
    var el = $($.render(template, item)).appendTo(root),
      detail = $(".detail", el);
    
    // toggle event
    $(".toggle", el).click(function() {
      simple.toggle(item.id);
    })

    function blur() {
      el.removeClass("detailing")
    }

    toggle(el, !!item.done);
    
    // show/hide detail
    detail.blur(blur).keydown(function(e) {
      var val = $.trim(this.value);
      if (e.which == 13 && val) {
        item.name = val;
        simple.detail(item);
      }

      if (e.which == 27) blur()
    })

    // Label double click event
    $("label", el).dbclick(function() {
      el.addClass("detailing");
      detail.focus()[0].select()
    })
    
    // Destroy detailing info
    $(".destroy", el).click(function() {
      detail.focus
    })
    

  }

})
