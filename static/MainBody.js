// 改变导航样式
$(function () {
    // 嵌入
    $('.code').click(function () {
        // 其余未选中去除样式类
        $('.chose').removeClass('chose');
        // 当前选中增加样式类
        $(this).addClass('chose');
        // 隐藏其他版块内容
        $('.display').removeClass('display').addClass('display_none');
        // 显示板块内容
        $('.UpLoadFrame').removeClass('display_none').addClass('display');
    });
    // 解码
    $('.decode').click(function () {
        // 其余未选中去除样式类
        $('.chose').removeClass('chose');
        // 当前选中增加样式类
        $(this).addClass('chose');
        // 隐藏其他版块内容
        $('.display').removeClass('display').addClass('display_none');
        // 显示板块内容
        $('.DecodeBlock').removeClass('display_none').addClass('display');
    });
    // 说明
    $('.info').click(function () {
        // 当前选中增加样式类
        // 其余未选中去除样式类
        $('.chose').removeClass('chose');
        // 当前选中增加样式类
        $(this).addClass('chose');
        // 隐藏其他版块内容
        $('.display').removeClass('display').addClass('display_none');
        // 显示板块内容
        $('.InfoBlock').removeClass('display_none').addClass('display');
    });
    // 合作/联系
    $('.contact').click(function () {
        // 其余未选中去除样式类
        $('.chose').removeClass('chose');
        // 当前选中增加样式类
        $(this).addClass('chose');
        // 隐藏其他版块内容
        $('.display').removeClass('display').addClass('display_none');
        // 显示板块内容
        $('.ContactBlock').removeClass('display_none').addClass('display');
    });
    // 下载
    $('.download').click(function () {
        // 其余未选中去除样式类
        $('.chose').removeClass('chose');
        // 当前选中增加样式类
        $(this).addClass('chose');
        // 隐藏其他版块内容
        $('.display').removeClass('display').addClass('display_none');
        // 显示板块内容
        $('.DownLoadFrame').removeClass('display_none').addClass('display');
    });
});

//剪贴板复制
function CopyEmail()
    {
        var mail=document.getElementById('mail').innerText;
        var oInput = document.createElement('input');
        oInput.value = mail;
        document.body.appendChild(oInput);
        oInput.select(); // 选择对象
        document.execCommand('copy'); // 执行浏览器复制命令
        oInput.className = 'oInput';
        oInput.style.display='none';
        alert('复制成功');
    }

// 文件上传
function upload()
    {
        $('#file_button').click();
    }
function upload_start(){
        var file = document.getElementById('file_button');
        // 判断是否中文件
        if(file.files[0] == undefined){
				alert('请先上传图片，再点击开始');
			}else{
            // 判断文件类型
                var file_value = file.value;
                var index = file_value.lastIndexOf('.');
                var file_type = file_value.substring(index);
                // 文件类型判断
                if(file_type == '.jpg' || file_type == '.png' || file_type == '.jpeg'){
                    // 文件大小判断
                    var file_size = file.files[0].size;
                    if(file_size > 2097139){
                        alert('图片大于2MB，请重新上传');
                    }else{
                        //1到15位英文，空格组成
                        var verify = /^[A-Za-z ]{1,15}$/;
                        var code_str = document.getElementById("code_filed").value;
                        //水印码校验
                        if (verify.test(code_str)){
                            $('.warning').text("正在处理");
                            $('#submit_button').click();
                        }else {
                            alert('请输入1至15位英文或空格组成的水印码');
                            document.getElementById("code_filed").value='';
                        }
                    }
            }
            else{
			    alert('只支持.jpg/.jpeg/.png格式图片，请重新选择');
            }
        }
    }
    
//文件下载
function image_delete(name){
    $.post('/done',{data:name}, function (result) {
        window.location.href=result
    });
}
function download_start(){
    $('.image_download_button').click();
}
function DownLoadImage(selector, name) {
    // 通过选择器获取img元素，
    var img = document.querySelector(selector);
    // 将图片的src属性作为URL地址
    var url = img.src;
    var a = document.createElement('a');
    var event = new MouseEvent('click');
    a.download = name;
    a.href = url;
    a.dispatchEvent(event);
    image_delete(name);
}
function leave_delete(name){
    $.post('/leave',{data:name}, function (result) {
        console.log(result);
    });
}

//解码上传
function decode_get()
    {
        $('#decode_button').click();
    }
function decode_start(){
        var file = document.getElementById('decode_button');
        // 判断是否中文件
        if(file.files[0] == undefined){
				alert('请先上传图片，再点击开始');
			}else{
            // 判断文件类型
                var file_value = file.value;
                var index = file_value.lastIndexOf('.');
                var file_type = file_value.substring(index);
                // 文件类型判断
                if(file_type == '.jpg' || file_type == '.png' || file_type == '.jpeg'){
                    // 文件大小判断
                    var file_size = file.files[0].size;
                    if(file_size > 2097139){
                        alert('图片大于2MB，请重新上传');
                    }else{
                        $('.warning2').text("正在解码");
                        $('#decode_submit').click();
                    }
            }
            else{
			    alert('只支持.jpg/.jpeg/.png格式图片，请重新选择');
            }
        }
    }