// 验证长度
function check_len(obj, min, max){
    return min <= obj.length && obj.length <= max;
}

// 验证邮箱
function check_email(obj){
    var re=/^\w+@[a-z0-9]+\.[a-z]+$/i;
    return re.test(obj);
}

// 验证手机号

function check_phone(obj) {
    let reg = /^1(3[0-9]|4[5,7]|5[0,1,2,3,5,6,7,8,9]|6[2,5,6,7]|7[0,1,7,8]|8[0-9]|9[1,8,9])\d{8}$/;
    return reg.test(obj)
}

// 验证两次密码
function check_password_repassword(password,repassword){
    return check_len(password,6,20) && check_len(repassword,6,20) && password === repassword;
}

function clean(obj){
    var ret = 0;
    $.each(obj, function (k) {
        if(!k){
            ret = 1
        }
    })
}

// 刷新头像
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

            // 提交前 做前端验证 减小服务器压力
        beforeSend:function (xmlHttpRequest) {

            if(check_len(data.password,6,20) && check_len(data.username,2,16)){
            }
            else {
                toastr.error("请正确填写用户名和密码");
                $("input[name=username],input[name=password]").addClass('has-error')
                xmlHttpRequest.abort()
            }
        },

            // 成功后回调函数
        success:function (data) {
            // 成功 跳转页面
            if (data.status) {
                location.href = data.msg;
            }
            // 失败 填充错误信息 修改样式
            else {
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

        // 提交前的数据验证
        beforeSend:function(xmlHttpRequest){

            // TODO 应该用反射减少冗余代码～～

            var flag = 1;
            if(!check_len(data.get('username'),2,16)){
                $("input[name=username]").addClass('has-error').next().text("必填项:2~16个字符");
                flag = 0;
            }
            if(!check_len(data.get("password"),6,20)){
                $("input[name=password]").addClass('has-error').next().text("必填项:2~16个字符");
                flag = 0;
            }
            if(!check_password_repassword(data.get("password"),data.get("repassword"))){
                $("input[name=repassword]").addClass('has-error').next().text("两次密码不一致");
                flag = 0;
            }
            if(!check_email(data.get("email"))){
                $("input[name=email]").addClass("has-error").next().text("邮箱格式不正确");
                flag = 0;
            }
            if(!check_phone(data.get("phone"))){
                $("input[name=phone]").addClass("has-error").next().text("手机号码不正确");
                flag = 0;
            }
            if(!check_len(data.get("nickname"),2,16)){
                $("input[name=nickname]").addClass("has-error").next().text("昵称应在2~16个字符");
                flag = 0;
            }

            // FIXME 需要整体优化前端代码  勿删
            // var data_dict = data.entries();
            //
            //     while (1){
            //         try {
            //           var i = data_dict.next();k = i.value[0];v = i.value[1];
            //         } catch(err) {
            //           break;
            //         }
            //     if(!eval("check_")){
            //
            //     }
            //     }

            if(flag){
                toastr.options = {
                  timeOut:3000,
                };
                toastr.success("注册数据提交中...")
            }

            else {
                // 阻止ajax 提交数据
                toastr.options = {
                  timeOut:3000,
                };
                toastr.info("数据残缺或格式不正确。");
                xmlHttpRequest.abort()
            }
        //
        },

        success: function (data) {
            if (data.status) {
                toastr.options = {
                    timeOut:100,
                    onHidden: function(){
                        location.href = data.msg;
                    }
                };
                toastr.info("注册成功！请马上到邮箱:"+data.email+"激活哦！")


            } else {
                toastr.error("注册信息有些不太对吧！看看提示再试吧！");
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

// 重置密码

$("#btn-pwdreset").on('click', function () {
    // 准备数据
    var data = {
        "password":$("input[name='password']").val(),
        "repassword":$("input[name='repassword']").val(),
        "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val()
    };

    $.post({
        url:'/user/pwdreset/1',
        data:data,
        beforeSend:function(xmlHttpRequest){

            if(!check_password_repassword(data.password,data.repassword)){
                toastr.error("密码应该6～20个字符且两次密码应该一致！");
                $("input[name=password]").addClass('has-error');
                xmlHttpRequest.abort()
            }
        },
        success:function (data){
            if(data.status){
                swal.fire(
                  '密码修改成功',
                  '确认后登陆！',
                  'success'
                );
                location.href = '/user/login'
            }
            else {
                toastr.options = {
                    timeOut:1000
                };
                toastr.error("密码应该6～20个字符且两次密码应该一致！");
                $.each(data.msg, function (k, v) {
                    $("input[name=" + k + "]").addClass('has-error').next().text(v)
                })
            }
        }

    })

});


$("#btn-go-login").on('click', function () {
    alert("111");
    location.href = '/user/login';
    alert("123")
});