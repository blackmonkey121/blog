(function($){
    // 隐藏 MarkDown
    var $contentMd = $("#div_id_content_md");
    var $contentCk = $("#div_id_content_ck");
    $contentMd.hide();
    // 拿到 type_editor 值
    function get_type_editor(){
        return $("input[autocomplete=off]").prev().data('value')
    }
    // 给选择元素绑定点击事件
    $("#id_editor_type").on("change", function () {
        if(get_type_editor()){
            $contentCk.show();
            $contentMd.hide();
        }else {
            $contentCk.hide();
            $contentMd.show();
        }
    })

})(jQuery);