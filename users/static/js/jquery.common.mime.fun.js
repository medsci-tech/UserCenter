/**
 * 基于jQuery的方法
 * author zhaiyu
 * startDate 20160511
 * updateDate 20160511
 */

console.log('jq-common-mime');

/**
 * 禁用启用等按钮的提交操作
 * @param statusType string | eg:'#div'
 * @param form string | eg:'#div'
 * @param val
 * @param location
 */
subActionStatusForMime = function (form, statusType, val, location) {
    $(statusType).val(val);
    console.log(val);
    $(form).submit();
    swal({
        title: "成功",
        type: "success",
        confirmButtonColor: "#1ab394",
        confirmButtonText: "确定",
        closeOnConfirm: false
    }, function () {
        window.location.href = location;
    });
    swal("已禁用！", "", "success");
};

/**
 * 判断多选框是否有勾选，有勾选返回true，没有则弹窗提示并返回false
 * @param check array
 * @returns {boolean}
 */
verifyCheckedForMime = function (check) {
    var checked = 0;
    for(var i =0; i < check.length; i++){
        if(check[i].checked == true){
            checked++;
        }
    }
    if(0 == checked){
        swal('未选择','请勾选需要操作的信息');
        return false;
    }else {
        return true;
    }
};

/**
 * ajax提交请求
 * @param type
 * @param url
 * @param data
 * @param location
 */
subActionAjaxForMime = function (type, url, data, location) {
    $.ajax({
        type: type,
        url: url,
        data: data,
        success: function(res){
            if(res.code == 200){
                swal({
                    title: "成功",
                    type: "success",
                    confirmButtonColor: "#1ab394",
                    confirmButtonText: "确定",
                    closeOnConfirm: false
                }, function () {
                    window.location.href = location;
                });
            }else {
                swal({
                    title: "失败",
                    text: res.msg,
                    type: "warning",
                    confirmButtonColor: "#1ab394",
                    confirmButtonText: "确定",
                    closeOnConfirm: false
                });
            }
        }
    });
};

/**
 *  获取dom列表的值
 * @param dataList
 * @returns {Array}
 */
var getDataListForMime = function(dataList) {
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
