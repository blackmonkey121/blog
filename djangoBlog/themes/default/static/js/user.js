
const $speCharReg = new RegExp("[`~!@#$^&*()=|{}':;',\\[\\].<>《》/?~！@#￥……&*（）——|{}【】‘；：”“'。，、？ ]");
const $emailReg = /^\w+@[a-z0-9]+\.[a-z]+$/i;
const $phoneReh = /^1(3[0-9]|4[5,7]|5[0,1,2,3,5,6,7,8,9]|6[2,5,6,7]|7[0,1,7,8]|8[0-9]|9[1,8,9])\d{8}$/;

// 更新头像
$("#id_avatar").on("change", function () {
    var fileReader = new FileReader();
    fileReader.readAsDataURL(this.files[0]);
    fileReader.onload = function () {
        $(".input-line img").attr("src", fileReader.result);
    }
});

// 清除错误提示
$("input").on('focus', function () {
    $(this).next().text('')
});

// 获取数据提交的url
var url = $("#app-data").data('url');

// 是否发送表单数据 数据验证通过，为0 失败 为1
var sendFlag = 0;
var passWordStr = '';
// 获取表单数据并验证是否规范，规范则返回数据源，不规范则写入错误信息 并将sendFlag 设为 真
function get_username(obj) {
    let $userName = $(obj);
    let $userNameStr = $userName.val();
    let $lengthUserName = $userNameStr.length <= 16 && $userNameStr.length >= 2;
    let $charUserName = !$speCharReg.test($userNameStr);
    if ($lengthUserName && $charUserName) {
        return $userNameStr
    } else {
        $userName.next().text('用户名应在2～16个字符，且不能存在特殊字符');
        sendFlag = 1
    }
}

function get_password(obj) {
    let $passWord = $(obj);
    passWordStr = $passWord.val();
    let $lengthPassWord = passWordStr.length <= 16 && passWordStr.length >= 6;
    let $charPassWord = !$speCharReg.test(passWordStr);
    if ($lengthPassWord && $charPassWord) {
        return passWordStr
    } else {
        $passWord.next().text('密码应在6～16个字符，且不能存在特殊字符');
        sendFlag = 1

    }

}

function get_repassword(obj) {
    let $re_passWord = $(obj);
    let $re_passWordStr = $re_passWord.val();
    let $lengthRePassWord = $re_passWordStr.length <= 16 && $re_passWordStr.length >= 6;
    let $charRePassWord = !$speCharReg.test($re_passWordStr);

    if ($re_passWordStr !== passWordStr) {
        $re_passWord.next().text('两次密码不一致');
        sendFlag = 1

    }

    if ($lengthRePassWord && $charRePassWord) {
        return $re_passWordStr
    } else {
        $re_passWord.next().text('密码应在6～16个字符，且不能存在特殊字符');
        sendFlag = 1

    }
}

function get_email(obj) {
    let $email = $(obj);
    let $emailStr = $email.val();
    let $charEmail = $emailReg.test($emailStr);
    if ($charEmail) {
        return $emailStr
    } else {
        $email.next().text('邮箱格式不正确');
        sendFlag = 1
    }
}

function get_phone(obj) {
    let $phone = $(obj);
    let $phoneStr = $phone.val();
    let $charPhone = $phoneReh.test($phoneStr);
    if ($charPhone) {
        return $phoneStr
    } else {
        $phone.next().text('手机号码格式不正确');
        sendFlag = 1
    }
}

// 按钮样式
var $btn = $('.button input');

$btn.mousedown(function () {
    $(this).css('background-color', '#555');
});

$btn.mouseover(function () {
    $(this).css('background-color', '#888');
    $(this).css('color', '#fff')
});

$btn.mouseout(function () {
    $(this).css('background-color', '#fff');
    $(this).css('color', '#888');
});

$btn.mouseup(function () {
    $(this).css('background-color', '#888');
    $(this).css('color', '#fff')
});

// 登陆
$('input[value="登陆"]').on('click', function () {
    var data = {
        "username": get_username("#id_username"),
        "password": get_password("#id_password"),
        "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
    };

    // 发送登陆数据 post
    $.post({
        url: url,
        data: data,

        // 检查表单数据是否通过验证
        beforeSend: function (xmlHttpRequest) {
          if (sendFlag) {
                swal.fire(
                    '账号或密码格式不正确',
                    '按照提示更正后再试！',
                    'error'
                );
                sendFlag = 0;
                xmlHttpRequest.abort()
            }
        },

        // 成功回调函数
        success: function (data) {
            // 成功 跳转页面
            if (data.status) {
                location.href = data.msg;
            }
            // 失败 填充错误信息 修改样式
            else if(data.check) {
                }else {
                swal.fire(
                    '账号或密码不正确',
                    '注意区分大小写哦！',
                    'error'
                );
            }
                   $.each(data.msg, function (k, v) {
                    $('#id_' + k).next().text(v)
                })
            }
        ,

    });

});

// 注册
$('input[value="注册"]').on('click', function () {
    // 准备ajax 数据
    var data = new FormData();

    data.append("username", get_username("#id_username"));
    data.append("password", get_password("#id_password"));
    data.append("repassword", get_repassword("#id_repassword"));
    data.append("email", get_email("#id_email"));
    data.append("phone", get_phone("#id_phone"));
    data.append("nickname", $("input[name=nickname]").val());
    data.append("avatar", $("#id_avatar")[0].files[0]);
    data.append("csrfmiddlewaretoken", $("[name='csrfmiddlewaretoken']").val());

    $.post({
        url: url,
        data: data,
        processData: false,   // jQuery不处理数据
        contentType: false,  // jQuery不要设置MIME

        // 提交前的数据验证
        beforeSend: function (xmlHttpRequest) {

            if (sendFlag) {
                swal.fire(
                    '注册数据错误',
                    '请检查标记的信息是否符合规范',
                    'error'
                );
                sendFlag = 0;
                xmlHttpRequest.abort()
            }


        },

        success: function (data) {
            if (data.status) {
                swal.fire({
                    title: '注册成功',
                    text: "如果不出意外，激活邮件已发至您的电子邮箱:" + data.msg["email"] + "! 请您尽快激活。激活链接有效时长仅为30分钟。如果未收到邮件，它可能被您默认的扔进了垃圾箱。",
                    type: 'success',
                    showCancelButton: true,
                    confirmButtonColor: '#63dbff',
                    cancelButtonColor: '#5e5e5e',
                    confirmButtonText: 'Go Login'
                }).then(function (isConfirm) {
                    if (isConfirm.value) {
                        location.href = data.msg["url"];
                    }
                });
            } else {

                swal.fire(
                    "错误提示",
                    "仔细阅读输入框后的提示，更正后再试，如有疑问，点右上角联系我们。",
                    "error"
                );

                $.each(data.msg, function (k, v) {
                    $("#id_" + k).next().text(v)
                })
            }
        },
    });

});

// 修改密码
$('input[value="提交修改"]').on('click', function () {
    var data = {
        "email": get_email("#id_email"),
        "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
    };

    // 发送登陆数据 post
    $.post({
        url: url,
        data: data,

        beforeSend: function (xmlHttpRequest) {
            if (sendFlag) {
                swal.fire(
                    '邮箱不正确',
                    '确保您写入的是正确的邮箱地址',
                    'error'
                );
                sendFlag = 0;
                xmlHttpRequest.abort()
            }
        },

        // 成功回调函数
        success: function (data) {
            // 成功 跳转页面
            if (data.status) {

                swal.fire({
                    title: '提交成功',
                    text: "改密邮件已发至您的电子邮箱:" + data.msg["email"] + "! 请您尽快前往修改。激活链接有效时长仅为30分钟。如果未收到邮件，它可能被您默认的扔进了垃圾箱。",
                    type: 'success',
                    showCancelButton: true,
                    confirmButtonColor: '#63dbff',
                    cancelButtonColor: '#5e5e5e',
                    confirmButtonText: 'Go Login'
                }).then(function (isConfirm) {
                    if (isConfirm.value) {
                        location.href = data.msg['url'];
                    }
                });


            }
            // 失败 填充错误信息 修改样式
            else {
                swal.fire({
                    title: '邮件发送失败',
                    text: "您提供的电子邮箱:" + data.msg["email"] + "! 尚未注册，点击\"Go Regist\"前往注册。",
                    type: 'info',
                    showCancelButton: true,
                    confirmButtonColor: '#63dbff',
                    cancelButtonColor: '#5e5e5e',
                    confirmButtonText: 'Go Regist'
                }).then(function (isConfirm) {
                    if (isConfirm.value) {
                        location.href = data.msg['url'];
                    }
                });
            }
        },

    });

});

// 重置密码
$('input[value="重置密码"]').on('click', function () {
    var data = {
        "email": get_email("#id_email"),
        "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),
        "new_password": get_password("#id_new_password"),
        "new_re_password": get_repassword("#id_new_re_password")
    };

    var url = $("#app-data").data('url');

    // 发送登陆数据 post

    $.post({
        url: url,
        data: data,

        // 提交前 做前端验证 减小服务器压力
        beforeSend: function (xmlHttpRequest) {

            if (sendFlag) {
                swal.fire(
                    '邮箱不正确',
                    '密码不不合规或两次密码不一致！',
                    'error'
                );
                sendFlag = 0;
                xmlHttpRequest.abort()
            }
        },

        // 成功回调函数
        success: function (data) {
            // 成功 跳转页面
            if (data.status) {

                swal.fire({
                    title: '密码修改成功',
                    text: "密码修改成功，点击\"Go Login\"将跳转至登陆页面！",
                    type: 'success',
                    showCancelButton: true,
                    confirmButtonColor: '#63dbff',
                    cancelButtonColor: '#5e5e5e',
                    confirmButtonText: 'Go Login'
                }).then(function (isConfirm) {
                    if (isConfirm.value) {
                        location.href = data.msg["url"];
                    }
                });
            }
            // 失败 填充错误信息 修改样式
            else {
                swal.fire({
                    title: '问题提示',
                    text: data.msg,
                    type: 'info',
                    showCancelButton: true,
                    confirmButtonColor: '#63dbff',
                    cancelButtonColor: '#5e5e5e',
                    confirmButtonText: 'OK '
                })
            }

            $.each(data.msg, function (k, v) {
                $('#id_' + k).next().text(v)
            })

        },

    });

});

// 动画效果
$.ready($(".input-line").animate({left: '0', opacity: '0.7',}),
    $("#left").animate({left: '20px', opacity: '0.5',}));




