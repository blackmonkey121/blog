// show comment area
$("#plus-button").on('click', function () {
    $("#comment-body").css('display', 'block');
});

// get datatime
function getCurrentDate(date) {
    var y = date.getFullYear();
    var m = date.getMonth() + 1;
    var d = date.getDate();
    var h = date.getHours();
    var min = date.getMinutes();
    var s = date.getSeconds();
    var str = y + '年' + (m < 10 ? ('0' + m) : m) + '月' + (d < 10 ? ('0' + d) : d) + '日  ' + (h < 10 ? ('0' + h) : h) + ':' + (min < 10 ? ('0' + min) : min) + ':' + (s < 10 ? ('0' + s) : s);
    return str;
}


// make comment area disappear
function disappear() {
    $("#comment-body").css('display', 'none').find('textarea').val('')
}

// submit
$(".submit-comment").on('click', function () {

    var extendData = $("#extend-data");
    // get data
    var data = {
        "content": $("textarea").val(),
        "target_id": extendData.data('target_id'),
        "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
    };

    // post submit data
    $.post({
        url: extendData.data('url'),
        data: data,

        // check data for post
        beforeSend: function (xmlHttpRequest) {
            if (!data.content || data.content.length > 200) {
                xmlHttpRequest.abort();
                swal.fire(
                    "评论失败～！评论不能为空，也不能超过200个字符啊！亲！",
                    "error"
                )
            }
            if ($("#extend-data").data('user') === '') {
                swal.fire({
                    title: '还没登陆吧！',
                    text: '是否去登陆页面呢？亲！',
                    type: 'info',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: '确定！',
                    cancelButtonText: "取消"
                }).then(function (reject) {
                    if (reject.value) {
                        location.href = '/user/login'
                    }
                })
            }

        },

        success: function (ret_data) {
            if (ret_data) {
                // 隐藏添加评论区
                disappear();
                // TODO:动态插入，不能刷新页面。每次都多请求一次页面
                // 收集新评论数据
                // 生成标签
                // 新评论添加到最顶部

            } else {
                swal.fire(
                    "提交失败了",
                    "哎呀 失败了！"
                )
            }
        }

    })

});