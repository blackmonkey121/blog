$(function () {
    var $extendData = $("#extend-data");

    var $comment = $('#comment-body');

    // show comment area
    $("#plus-button").on('click', function () {
        $comment.slideDown(300);
        $('#add-comment-content').focus()
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
    $("#add-comment-content").on('blur', function () {
        $comment.slideUp(300)
    });

    $(".cancel-comment").click(function () {
        $comment.slideUp(300)
    });

// submit
    $(".submit-comment").on('click', function () {

        // get data
        var data = {
            "content": $("textarea").val(),
            "target_id": $extendData.data('target_id'),
            "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
        };

        // post submit data
        $.post({
            url: $extendData.data('url'),
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
                if ($.cookie('user') === undefined) {
                    xmlHttpRequest.abort();
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
                            location.href = '/user/login/'
                        }
                    })
                }

            },

            success: function (ret_data) {
                if (ret_data) {
                    // 隐藏添加评论区
                    $comment.slideUp(300);
                    // 收集新评论数据 生成标签
                    var $avatar = $('<img>').attr('src', $extendData.data('avatar'));    // url
                    var $commentContext = $('<p></p>').text($("textarea").val());
                    var $lineDiv = $('<div class="comment-body clearfix">').append($avatar, $commentContext);

                    var $span1 = $('<span class="list-comment-nickname"></span>').text($extendData.data('nickname'));
                    var $span2 = $('<span><i class="fa fa-clock-o"></i></span>').text(getCurrentDate(new Date()));
                    var $span3 = $('<span class="up"><i class="fa fa-thumbs-up"></i> 赞 0 </span>');
                    var $span4 = $('<span class="down"><i class="fa fa-thumbs-down"></i> 踩 0 </span>');
                    var $lineP = $('<p class="comment-cookies">').append($span1, $span2, $span3, $span4);

                    var $line = $('<div class="comment-line">').append($lineDiv, $lineP).hide();

                    // 新评论添加到最顶部
                    $('#list-comment').prepend($line);
                    $line.slideDown(300)

                } else {
                    swal.fire(
                        "提交失败了",
                        "哎呀 失败了！"
                    )
                }
            }

        })

    });

// comment click start
    $(".comment-cookies [cid]").click(function () {

        var data = {
            "cid": $(this).attr('cid'),
            "type": $(this).attr('class'),
            "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
        };

        var $this = $(this);

        $.post({
            url: $extendData.data('point'),
            data: data,

            // check data for post
            beforeSend: function (xmlHttpRequest) {
                if ($.cookie('user') === undefined) {
                    xmlHttpRequest.abort();
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
                            location.href = '/user/login/'
                        }
                    })
                }
            },

            success: function (data) {
                if (data.status) {
                    // 修改点赞数
                    let num = parseInt($this.find('span').text()) + 1;
                    $this.find('span').text(num)
                } else {
                    swal.fire(
                        data.msg,
                        "哎呀 失败了！"
                    )
                }
            }

        })

    });

// article click start
    $("#thumb [cid]").click(function () {

        var data = {
            "cid": $(this).attr('cid'),
            "type": $(this).attr('class'),
            "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
        };

        var $this = $(this);

        $.post({
            url: $("#detail").attr('href'),
            data: data,

            // check data for post
            beforeSend: function (xmlHttpRequest) {
                if ($.cookie('user') === undefined) {
                    xmlHttpRequest.abort();
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
                            location.href = '/user/login/'
                        }
                    })
                }
            },

            success: function (data) {
                if (data.status) {
                    // 修改点赞数
                    let num = parseInt($this.find('span').text()) + 1;
                    $this.find('span').text(num)
                } else {
                    swal.fire(
                        data.msg,
                        "哎呀 失败了！"
                    )
                }
            }

        })

    });

// add favorite
    $("#start").click(function () {
        if ($.cookie('user')) {
            let $title = $("#detail-title").text().replace(/\s+/g, "");
            let $href = location.href;
            swal.fire({
                title: '收藏信息',
                html:
                    '<input id="swal-input1" class="swal2-input" placeholder="名称" autofocus value=' + $title + ' >' +
                    '<input id="swal-input2" class="swal2-input" placeholder="akshdskadskfnds" disabled value=' + $href + '>',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: '确定！',
                cancelButtonText: "取消",
            }).then(function (result) {
                if (result.value) {
                    let data = {
                        "title": $title,
                        "href": $href,
                        "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()

                    };

                    $.post({
                        url: $extendData.data('favorite'),
                        data: data,

                        success: function (ret_data) {
                            if (ret_data) {
                                swal.fire({
                                    showConfirmButton: false,
                                    timer: 1000,
                                    type: 'success',
                                    title: '收藏成功'
                                })

                            } else {
                                swal.fire(
                                    "提交失败了",
                                    "哎呀 失败了！"
                                )
                            }
                        }

                    })

                }
            })
        } else {
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
                    location.href = '/user/login/'
                }
            })

        }
    })
});


