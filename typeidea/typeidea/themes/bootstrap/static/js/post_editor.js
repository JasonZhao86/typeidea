(function($){
    $content_md = $("#div_id_content_md");
    $content_ck = $("#div_id_content_ck");
    $is_md = $("input[name=is_md]");
    var switch_editor = function(is_md){
        if (is_md){
            $content_md.show();
            $content_ck.hide();
        }else{
            $content_ck.show();
            $content_md.hide();
        }
    }
    $is_md.on("click", function(){
        switch_editor(($(this).is(":checked")));
    });
    switch_editor($is_md.is(":checked"));
})(jQuery)