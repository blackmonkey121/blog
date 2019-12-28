$("#id_avatar").on("change", function () {
    var fileReader = new FileReader();
    fileReader.readAsDataURL(this.files[0]);
    fileReader.onload = function () {
        $("#avatar img").attr("src", fileReader.result);
        // console.log(fileReader.result)
    }
});

// 登陆

$("#btn-login").on('click', function () {
    // 准备 ajax 数据

    var data = {
        "username": $("input[name=username]").val(),
        "password": $("input[name=password]").val(),
        "save": $("input[name=isSave]").is(':checked'),
        "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
    };

    // ajax 发送登陆数据 post

        $.post({
        url: '/user/login',
        data: data,
            // 提交前 做前端验证
        beforeSend:function (xmlHttpRequest) {
            user = 2<data.username.length && data.username.length<18;
            pwd = 6<data.password.length && data.password.length<20;
            if(user && pwd){}
            else {
                toastr.error("请正确填写用户名和密码");
                xmlHttpRequest.abort()
            }
        },

        success:function (data) {
            if (data.status) {
                location.href = data.msg;
            } else {
                toastr.error("账号或密码错误，检查拼写错误或大小写！");
                $.each(data.msg, function (k, v) {
                    $("input[name=" + k + "]").addClass('has-error').next().text(v);
                })
            }
        },

    });

    // 修改错误样式  写入报错信息
    $(".control-line input").on('focus', function () {
        $(this).removeClass('has-error').next().text('')
    })
});

// 注册
$("#btn-regist").on('click', function () {

    // 准备ajax 数据
    var data = new FormData();

    data.append("username", $("input[name=username]").val());
    data.append("password", $("input[name=password]").val());              // var data = {
    data.append("repassword", $("input[name=repassword]").val());              //     "username": $("input[name=username]").val(),
    data.append("email", $("input[name=email]").val());              //     "password": $("input[name=password]").val(),
    data.append("phone", $("input[name=phone]").val());             //     "repassword": $("input[name=repassword]").val(),
    data.append("nickname", $("input[name=nickname]").val());              //     "email": $("input[name=email]").val(),
    data.append("avatar", $("input[name=avatar]")[0].files[0]);              //     "phone": $("input[name=phone]").val(),
    data.append("csrfmiddlewaretoken", $("[name='csrfmiddlewaretoken']").val());//     "nickname": $("input[name=nickname]").val(),

    $.post({
        url: '/user/regist',
        data: data,
        processData: false,   // 告诉jQuery不要处理我的数据
        contentType: false,  // 告诉jQuery不要设置content类型

        success: function (data) {
            if (data.status) {

                location.href = data.msg;
            } else {
                $.each(data.msg, function (k, v) {
                    $("input[name=" + k + "]").addClass('has-error').next().text(v)
                })
            }
        },
    });

    // 清除错误提示样式 和信息
    $(".control-line input").on('focus', function () {
        $(this).removeClass('has-error').next().text('')
    })

});

// 修改密码
$("#btn-resetpwd").on('click',function () {
    // 准备数据

    var data = new FormData;

    data.append('email', $('input[name=email]').val());
    data.append('password', $('input[name=password]').val());
    data.append('repassword', $('input[name=repassword]').val());
    data.append("csrfmiddlewaretoken", $("[name='csrfmiddlewaretoken']").val());

    // 发送数据

    $.post({
        url:'/user/resetpwd',
        data:data,
        processData: false,   // 告诉jQuery不要处理我的数据
        contentType: false,  // 告诉jQuery不要设置content类型
        beforeSend:function(){

        },
        success:function (data) {
            if(data.status){
                toastr.options={
                    "timeOut":1000,
                    "onHidden": function(){
                        location.href = '/user/login'
                    }
                };
                toastr.success(data.msg);
            }
            else {
                toastr.options = {
                    "timeOut": 1000,
                };
                toastr.error("邮箱不正确或两次密码不一致。","改密失败");

                $.each(data.msg, function (k, v) {
                    $("input[name=" + k + "]").addClass('has-error').next().text(v)
                })

            }
        }
    });

    // 清除错误提示样式 和信息
        $(".control-line input").on('focus', function () {
        $(this).removeClass('has-error').next().text('')
    })

});

//找回密码

$("#btn-forgetpwd").on('click',function () {
    // 准备数据

    // var data = new FormData;

    // data.append('email', $('input[name=email]').val());

    // 发送数据

    $.post({
        url:'/user/forgetpwd',
        data:{
            "email":$('input[name=email]').val(),
            "csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()
        },

        success:function (data) {
            if(data.status){
                toastr.options={
                    "timeOut":1000,
                    "onHidden": function(){
                        location.href = '/user/login'
                    }
                };
                toastr.success(data.msg);

            }
            else {
                $.each(data.msg, function (k, v) {
                    $("input[name=" + k + "]").addClass('has-error').next().text(v)
                })

            }
        }
    });

    // 清除错误提示样式 和信息
        $(".control-line input").on('focus', function () {
        $(this).removeClass('has-error').next().text('')
    })

});







