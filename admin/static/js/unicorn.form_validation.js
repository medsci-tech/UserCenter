/**
 * Unicorn Admin Template
 * Version 2.2.0
 * Diablo9983 -> diablo9983@gmail.com
 * edit by lxhui
**/
function ajaxSubmitForm() {
        var para = '';//组织参数
        var url = "/jajax/saveForm.py";
        $.ajax({
            type: "post",
            cache: false,
            dataType: "json",
            url: url,
            data: para,
            beforeSend: function(XMLHttpRequest){
                //do something before submit...
            },
            success: function(data, textStatus){
                //do something after submited...
            },
            complete: function(XMLHttpRequest, textStatus){
                //do something in the end...
            }
        });
    }
$(document).ready(function(){
	
	$('input[type=checkbox],input[type=radio]').iCheck({
    	checkboxClass: 'icheckbox_flat-blue',
    	radioClass: 'iradio_flat-blue'
	});
	
	$('select').select2();
	
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
				required: true,
				minlength:6,
				maxlength:20
			},
			pwd2:{
				required:true,
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
		d = $("#basic_validate").serializeArray();
		console.log(d);
/*			$(this).ajaxSubmit({  
                type:"post",  //提交方式  
                dataType:"json", //数据类型  
                url:"login.action", //请求url  
                success:function(data){ //提交成功的回调函数  
                    //alert(data.result);
					alert('ok')
                }  
            });  
            return false; *///不刷新页面
			//ajaxSubmitForm();
        },//这是关键的语句，配置这个参数后表单不会自动提交，验证通过之后会去调用的方法
		
	});
	/* 表单重置 */
	$("#reset").click(function() {
        validator.resetForm();
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
