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
        $('#FilePic').click();
        $('#FileUpload').submit();
    }