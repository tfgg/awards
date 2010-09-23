toaster_top = false;
gap = 10;
top_toaster = null;

function show_toaster(el) {
    el.show().css("opacity", "0");
    if(toaster_top)
        el.animate({opacity:"1", top:el.final_pos+"px"}, 1000);
    else
        el.animate({opacity:"1", bottom:el.final_pos+"px"}, 1000);
}

function hide_toaster(el) {
    el.fadeOut(1000, function(){ el.remove(); });
    if(top_toaster == el) top_toaster = null;
}

function add_corners(el) {
    el.css("-moz-border-radius-bottomleft", "10px")
    el.css("-moz-border-radius-bottomright", "10px")
    el.css("-moz-border-radius-topleft", "10px")
    el.css("-moz-border-radius-topright", "10px")
}

function toaster_message(msg) {
    el = $('<div class="toaster"><div class="toaster-inner">'+msg+'</div></div>').appendTo('#content');
    
    //el.click(function(){ hide_toaster(el); });
    
    pos = -el.height();
    if(top_toaster != null)
    {
        if(toaster_top)
            pos += top_toaster.final_pos + top_toaster.height();
        else
            pos += top_toaster.final_pos + top_toaster.height();
        
        top_toaster = el;
    }
    else
        top_toaster = el;
    
    if(toaster_top)
        el.css("top", pos+"px");
    else
        el.css("bottom", pos+"px");
    
    el.final_pos = pos+el.height()+gap;
    
    el.hide();
    
    add_corners(el);
    show_toaster(el);
    
    setTimeout(function(el) { hide_toaster(el); }, 10000, el);
    
    return el;
}

function make_award(award_name) {
    $.post('http://localhost/api/submit_award',
           { name: award_name, source: 'awards' },
           function(data) {
                data = jQuery.parseJSON(data);
                toaster_message("<a href='http://localhost/users/" + data['user'] + "'>Awarded '" + award_name + "' to " + data['user'] + "</a>");

                if(data['temporary_account']) {
                    toaster_message("Register your account here");
                }
          });
}
