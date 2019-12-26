$("#id_avatar").on("change", function () {
    var fileReader = new FileReader();
    fileReader.readAsDataURL(this.files[0]);
    fileReader.onload = function () {
        $("#avatar img").attr("src", fileReader.result);
        console.log(fileReader.result)
    }
});

