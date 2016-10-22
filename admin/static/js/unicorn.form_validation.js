/**
 * Unicorn Admin Template
 * Version 2.2.0
 * Diablo9983 -> diablo9983@gmail.com
 * edit by lxhui
**/

/**
 * 判断多选框是否有勾选，有勾选返回true，没有则弹窗提示并返回false
 * @param check array
 * @returns {boolean}
 */
var verifyChecked = function (check) {
	var checked = 0;
	for(var i =0; i < check.length; i++){
		if(check[i].checked == true){
			checked++;
		}
	}
	if(0 == checked){
		swal('未选择','请勾选需要操作的记录!');
		return false;
	}else {
		return true;
	}
};
/**
 *  获取dom列表的值
 * @param dataList
 * @returns {Array}
 */
var getDataList = function(dataList) {
    var list = [], j = 0;
    for(var i = 0; i < dataList.length; i++){
        var child = dataList[i];
        if(('radio' == child.type || 'checkbox' == child.type)){
            if(true == child.checked){
                list[j] = $(child).val();
                j++;
            }
        }else {
            list[i] = $(child).val();
        }
    }
    return list;
};
/* 定义常用ajax提交方法 */
var ajaxFun = function (para,url) {
	$.ajax({
		type: "post",
		cache: false,
		dataType: "json",
		url: url,
		data: para,
		beforeSend: function(XMLHttpRequest){

		},
		success: function(data, textStatus){
			 if(data.status > 0){
				swal({
					title: "保存成功",
					type: "success",
					confirmButtonColor: "#1ab394",
					confirmButtonText: "确定",
					closeOnConfirm: false
				}, function () {
					window.location.reload();
				});
			}else {
				swal({
					title: "保存失败",
					text: data.msg,
					type: "warning",
					confirmButtonColor: "#1ab394",
					confirmButtonText: "确定",
					closeOnConfirm: false
				});
			}
		},
		complete: function(XMLHttpRequest, textStatus){
			if($("#id")[0]){
				//$("#id").remove();
			}
		}
	});
}
$(document).ready(function(){
	$('input[type=checkbox],input[type=radio]').iCheck({
    	checkboxClass: 'icheckbox_flat-blue',
    	radioClass: 'iradio_flat-blue'
	});
	
	// 管理员表单验证
        var validator = $("#basic_validate").validate({
		rules:{
			required:{
				required:true
			},
			username:{
				required: true,
				minlength:2,
				maxlength:20
			},
			pwd:{
				required: false,
				minlength:6,
				maxlength:20
			},
			pwd2:{
				required:false,
				minlength:6,
				maxlength:20,
				equalTo:"#pwd"
			},
			email:{
				required:true,
				email: true
			},
			date:{
				required:true,
				date: true
			},
			url:{
				required:true,
				url: true
			}
		},
		errorClass: "help-inline",
		errorElement: "span",
		highlight:function(element, errorClass, validClass) {
			$(element).parents('.form-group').removeClass('has-success').addClass('has-error');
		},
		unhighlight: function(element, errorClass, validClass) {
			$(element).parents('.form-group').removeClass('has-error').addClass('has-success');
		},
		submitHandler:function(form) {
		param = $("#basic_validate").serialize();
                ajaxFun(param,'/admin/admin/save/');
        },//这是关键的语句，配置这个参数后表单不会自动提交，验证通过之后会去调用的方法
		
	});

	$("#number_validate").validate({
		rules:{
			min:{
				required: true,
				min:10
			},
			max:{
				required:true,
				max:24
			},
			number:{
				required:true,
				number:true
			}
		},
		errorClass: "help-inline",
		errorElement: "span",
		highlight:function(element, errorClass, validClass) {
			$(element).parents('.form-group').addClass('has-error');
		},
		unhighlight: function(element, errorClass, validClass) {
			$(element).parents('.form-group').removeClass('has-error');
			$(element).parents('.form-group').addClass('has-success');
		}
	});
	/* 密码验证 */
	$("#password_validate").validate({
		rules:{
			pwd:{
				required: true,
				minlength:6,
				maxlength:20
			},
			pwd2:{
				required:true,
				minlength:6,
				maxlength:20,
				equalTo:"#pwd"
			}
		},
		errorClass: "help-inline",
		errorElement: "span",
		highlight:function(element, errorClass, validClass) {
			$(element).parents('.form-group').addClass('has-error');
		},
		unhighlight: function(element, errorClass, validClass) {
			$(element).parents('.form-group').removeClass('has-error');
			$(element).parents('.form-group').addClass('has-success');
		}
	});
});
