/**
 * 基于jQuery的方法
 * author zhaiyu
 * startDate 20160511
 * updateDate 20160511
 */

console.log('jq-common-mime');

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

/**
 * 重置文件上传进度条状态
 * @param inputId
 */
var uploadDataReset = function (inputId) {
    $('#progress-' + inputId + ' .progress-bar').width(0).find('span').text('');
};

/**
 * 启用操作
 * @param check
 * @param stats_url
 * @param index_url
 */
var enableDataMultiple = function (check, stats_url, index_url) {
    swal({
        title: "您确定要启用选中的信息吗",
        type: "warning",
        showCancelButton: true,
        cancelButtonText: '取消',
        confirmButtonColor: "#23c6c8",
        confirmButtonText: "确定",
        closeOnConfirm: false
    }, function () {
        var data = {};
        data.selection = getDataListForMime(check);
        data.statusType = 'enable';
        console.log(data);
        subActionAjaxForMime('post', stats_url, data, index_url);
    });
};

/**
 * 禁用操作
 * @param check
 * @param stats_url
 * @param index_url
 */
var disableDataMultiple = function (check, stats_url, index_url) {
    swal({
        title: "您确定要禁用选中的信息吗",
        type: "warning",
        showCancelButton: true,
        cancelButtonText: '取消',
        confirmButtonColor: "#f8ac59",
        confirmButtonText: "确定",
        closeOnConfirm: false
    }, function () {
        var data = {};
        data.selection = getDataListForMime(check);
        data.statusType = 'disable';
        console.log(data);
        subActionAjaxForMime('post', stats_url, data, index_url);
    });
};
