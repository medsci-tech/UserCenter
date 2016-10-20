document.write("<script src='/static/plugins/city-picker/city-picker.data.js'></script>");
document.write("<script src='/static/plugins/city-picker/city-picker.js'></script>");

/**
 *  修改数据前获取数据信息
 * author zhaiyu
 * startDate 20160510
 * updateDate 20160510
 * @param value
 * @param parentBom
 */
getRegionDefault = function (value,parentBom) {
    if(parentBom){
        parentBom = '#' + parentBom + ' ';
    }else {
        parentBom = '';
    }
    var pickerHtml = '';
    var pickerSpan = $(parentBom + '[data-toggle="city-picker"]').next();
    if (value.province) {
        pickerHtml += '<span class="select-item" data-count="province">' + value.province + '</span>' +
          '<input type="hidden" name="province" value="' + value.province + '">';
        if (value.city) {
            pickerHtml += '/<span class="select-item" data-count="city">' + value.city + '</span>' +
              '<input type="hidden" name="city" value="' + value.city + '">';
            if (value.area) {
                pickerHtml += '/<span class="select-item" data-count="district">' + value.district + '</span>' +
                  '<input type="hidden" name="district" value="' + value.district + '">';
            }
        }
        pickerSpan.find('.placeholder').css('display', 'none');
        pickerSpan.find('.title').css('display', 'inline').html(pickerHtml);
    }else {
        pickerSpan.find('.placeholder').css('display','');
        pickerSpan.find('.title').css('display','none').html(pickerHtml);
    }
};

/**
 *  编辑数据前初始化数据--一般为添加操作
 * author zhaiyu
 * startDate 20160510
 * updateDate 20160510
 * @param parentBom
 */
getRegionInit = function (parentBom) {
    if(parentBom){
        parentBom = '#' + parentBom + ' ';
    }else {
        parentBom = '';
    }
    var pickerHtml = '';
    var pickerSpan = $(parentBom + '[data-toggle="city-picker"]').next();
    pickerSpan.find('.placeholder').css('display','');
    pickerSpan.find('.title').css('display','none').html(pickerHtml);
};