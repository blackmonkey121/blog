// 注销
$("#li-logout").on('click', function () {
    $.get({
        url:'/user/logout',
        success:function () {
                toastr.options={
                    "timeOut":100,
                    "positionClass": "toast-top-full-width",
                    "onHidden": function(){
                        location.href = '/user/login'
                    }
                };
                toastr.success("注销成功");
        }
    })
});


// 改密
$("#li-resetpwd").on('click', function () {
    location.href = '/user/resetpwd'
});