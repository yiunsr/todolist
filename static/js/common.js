
//// django 에서 ajax 로 post 를 보낼 때 csrf 문제로 생기는 버그 수정
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
    	var csrftoken = getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


var _GLOBAL_DICT = {
  loadingQueue : []
};

//// ` 를 사용해보려 했으나 IE11 에서 큰 오류가 발생해서 + 기호를 이용함
//// http://bootsnipp.com/index.php/snippets/featured/quotwaiting-forquot-modal-dialog
var _$dialog = jQuery(
  '<div class="modal fade"  id="loadingModal" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true" style="padding-top:15%;">' +
  '<div class="modal-dialog modal-m">' +
  '<div class="modal-content">' +
    '<div class="modal-header"><h3 style="margin:0;" class="loading"></h3></div>' +
    '<div class="modal-body">' +
      '<div class="progress">' +
        '<div class="progress-bar bg-success progress-bar-striped progress-bar-animated" style="width: 100%"></div></div>' +
    '</div>' +
  '</div></div></div>');

var _$alert = jQuery(
  '<div class="modal fade" id="alertModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">'+
    '<div class="modal-dialog">'+ 
      '<div class="modal-content">'+
        '<div class="modal-header"> <h4 class="modal-title" id="myModalLabel">Modal title</h4> </div>'+
        '<div class="modal-body"></div>' +
        
        '<div class="modal-footer">'+
          '<button type="button" class="btn btn-primary" data-dismiss="modal" data-id="close">Close</button>'+
        '</div>' +
      '</div>'+
    '</div>'+
  '</div>'
);


var _$confirm = jQuery(
  '<div class="modal fade" id="confirmModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">' +
    '<div class="modal-dialog">' +
      '<div class="modal-content">' +
        '<div class="modal-header">' +
          '<h4 class="modal-title" id="myModalLabel">Modal title</h4>' +
        '</div>' +
        
        '<div class="modal-body"></div>' +
        
        '<div class="modal-footer">' +
          '<button type="button" class="btn btn-primary" data-id="ok">확인</button>' +
        '</div>' +
      '</div>' +
    '</div>' +
  '</div>'
);

_$dialog.appendTo( "body" ); _$dialog = jQuery("#loadingModal");
_$alert.appendTo( "body" ); _$alert = jQuery("#alertModal");
_$confirm.appendTo( "body" ); _$confirm = jQuery("#confirmModal");

var _DEBUG_INFO = {
  // 차후 chromedirver 같은 툴로 디버깅용
  alertLog : ""  
};

jQuery.extend({

  /**
   * jQuery.getUrlVar(name)
   * 현재 URL에 대해 parameter 값을 가져온다. 
   * ex) 현재 URL : http://localhost/test?param1=value1&param2=1234#tag 일 때
   *    jquery.getUrlVar("param1") => "value1" 
   * 
   * @param {String} name :  얻고 싶은 parameter key
   * @return {Object}  : parameter 의 value
   * 
   * 참고 : https://davidwalsh.name/query-string-javascript
   */
  getUrlVar: function(name){
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
  },

  /**
   * jQuery.reload()
   * 페이지 리로드
   * 
   * @return {Object}  : Nothing
   */
  reload: function(){
    /// reload 하는 시간이 늦을 경우 화면내에 클릭이나 입력이 들어갈 수 있으므로 강제로 막는다. 
    jQuery.pushLoadingQueue("reload");
    location.reload();
  },

  move: function(url){
    /// 페이지 이동 
    jQuery.pushLoadingQueue("reload");
    window.location.href = url;
  },

  /**
   * jQuery.alert("제목", "내용")
   * Layer Popup 을 뛰운다. 
   * 
   * @param {String} title :  Layer Popup에 대한 제목
   * @param {String} body :  Layer Popup에 대한 내용
   * @param {function} callback :  Layer Popup의 close 버튼을 눌렀을 때 이후에 동작해야 하는 callback 동작
   *  이를테면, 에러 팝업 뒤, 파업창 close 한 두 에러 발생한 input 으로 포커스를 이동시켜야 할 때. 
   * @param {String} hideClose :  Layer Popup의 close 버튼을 숨긴다.
   *  이 값이 설정되는 것은 해당 페이지를 refresh 해야 하거나 다른 페이지에 접속해야 하는 경우에만 발생한다.
   * 
   * 
   * @return {Object}  : Nothing
   * 
   * 참고 : https://davidwalsh.name/query-string-javascript
   * 알려진 버그 : alert창 중복 사용 안됨.
   */
  alert : function(title, body, callback, hideClose ){
    _$alert.find(".modal-title").html(title);
    _$alert.find(".modal-body").html(body);
    _$alert.modal('show');
    
    _$alert.find("[data-id=close]").bind( "click" , function(){
      jQuery("#alertModal [data-id=close]").unbind( "click");
      if(callback)
        callback();
    });
    if( hideClose)
    _$alert.find("[data-id=close]").hide();
    else{
    	_$alert.find("[data-id=close]").show();
    	_DEBUG_INFO["alertLog"] = body;
    }
    
  },

  /**
   * jQuery.confirm(title, body, callbacs)
   * 예, 아니오가 있는 확인 창
   * 
   * 
   * 
   * @param {string} title :  confirm Layer popup의 title 
   * @param {string} body :  confirm Layer popup의 본문
   * @param {function} callback :  예, 아니오 결과를 전달하는 callback
   * @return {Object}  : Nothing
   * 
   * 참고 : https://davidwalsh.name/query-string-javascript
   */
  confirm : function(title, body, callback){
    _$confirm.find(".modal-title").text(title);
    _$confirm.find(".modal-body").text(body);
    _$confirm.modal('show');
    
    _$confirm.find("[data-id=close]").click(function() {
      jQuery("#confirmModal [data-id=close]").unbind( "click");
      jQuery("#confirmModal").modal('hide');
      if(callback)
        callback( false );
    });
    
    _$confirm.find("[data-id=ok]").click(function() {
      jQuery("#confirmModal [data-id=ok]").unbind( "click");
      jQuery("#confirmModal").modal('hide');
      if(callback)
        callback( true );
    });
  },

  /**
   * jQuery.pushLoadingQueue(key, progress)
   * Loading Progressive Bar 를 보여주기 위해 네트워크로 요청한 리스트 관리 기능  
   * 서버로 request 한 것이 있으면 "method:path" 형태로 저장해 두어야 한다. 
   * 
   * 
   * @param {string} key :  리스트에 쌓을 데이터 ex) "POST:/users/login"
   * @param {string} progress :  요청한 request 가 progress bar 의 percent 기능을 사용할 때 true 임
   * @return {Object}  : Nothing
   * 
   * 참고 : https://davidwalsh.name/query-string-javascript
   */
  pushLoadingQueue : function(key, progress){
    percent = 100;
    _GLOBAL_DICT['loadingQueue']
    if( progress) percent = 0;
    if( _GLOBAL_DICT['loadingQueue'].length == 0 ){
      jQuery.loading(true, percent);
    }
    _GLOBAL_DICT['loadingQueue'].push(key);
  },

  /**
   * jQuery.popLoadingQueue(key, progress)
   * Loading Progressive Bar 를 보여주기 위해 네트워크로 요청한 리스트 관리 기능  
   * 
   * @param {string} key :  리스트에 remove 할 데이터 ex) "POST:/users/login"
   * @return {Object}  : Nothing
   * 
   * 참고 : https://davidwalsh.name/query-string-javascript
   */
  popLoadingQueue : function(key){
    var index = _GLOBAL_DICT['loadingQueue'].indexOf(key);
    if (index > -1) {
      _GLOBAL_DICT['loadingQueue'].splice(index, 1);
    }
    if( _GLOBAL_DICT['loadingQueue'].length == 0 ){
    	//// Timeout 한 후에 다시 왔을 때도 queue 가 비었을 때만 정말 hide
    	setTimeout(function() {  
    		 if ( _GLOBAL_DICT['loadingQueue'].length == 0 ) 
    			 jQuery.loading(false);
      }, 500); 
      //// 시간을 주지 않았을 경우 bootstrap 4.0 에서는 modal 이 보였다가 다시 사라지지 않는 현상 발생함
      //// 아주 짧은시간 show, hide 하게 되면 내부적인 show 로직이 hide 가 불려서 문제가 발생해서 시간차이를 강제로 둠.
      
    }
  },

  
  /**
   * jQuery.loading(bShow, percent)
   * Loading Progressive Bar 를 보여주기 위해 네트워크로 요청한 리스트 관리 기능  
   * 
   * @param {string} bShow :  Loading 팝업을 show, hide 설정
   * @param {string} percent :  Loading 팝업을 보여줄 때 process 의 % 설정
   * @return {Object}  : Nothing
   * 
   * 참고 : https://davidwalsh.name/query-string-javascript
   */
  loading : function(bShow, percent ){
    var message = "Loading";
    
    if ( !percent )
      percent = 100;
    _$dialog.find('.progress-bar').css("width", percent + "%");
   
    if(bShow){
        var settings = jQuery.extend({
        dialogSize: 'm',
        progressType: '',
        onHide: null // This callback runs after the dialog was hidden
      });
      if (settings.progressType) {
        _$dialog.find('.progress-bar').addClass('progress-bar-' + settings.progressType);
      }
      _$dialog.find('h3').text(message);
      // Adding callbacks
      if (typeof settings.onHide === 'function') {
        _$dialog.off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
          settings.onHide.call(_$dialog);
        });
      }
      // Opening dialog
      _$dialog.modal('show');
      console.log("loading dialog show");
    
    }
      
    else {
      _$dialog.modal('hide');
      console.log("loading dialog hide");
    }
  },

  /**
   * jQuery.request()
   * Server와 통신할 때는 이 Method 를 이용해야 한다. 
   * 
   * @param {String} method :  HTTP Request method 로 GET, POST, PUT, DELETE 가 있다. 
   * @param {String} path :  ajax 를 요청한 path로 "/"로 시작해야 한다. 
   * @param {Dict} data :  { key1: "value1", ... } 형태의 parameter 
   *             jQuery(selector).getParam 러 쉽게 얻을 수 있다.
   * @param {String} callback :  request 성공시의 callback 함수
   * @param {Dict} optData :  추가 옵션,  jQuery.ajax 에 대해 추가 parameter 를 전달 한다. 
   * @return {Object}  : jQuery.ajax 에 대한 리턴, 이 값을 이용해서 jQuery.when 인자로 이용할 수 있다. 
   */
  request : function(method, path, data, callback, optDate){
    method = method.toUpperCase();
    var percent = 100;
    if ( optDate  &&  "processData" in optDate && optDate.processData == false ) 
      percent = 0;
    var key = method + ":" + path;
    jQuery.pushLoadingQueue(key, percent);
    
    return jQuery.ajax({type: method, 
      url: path,
      data: data,
      dataType: 'json',
      cache : false,
      success: function (data, textStatus,  jqXHR ) {
        //
        var path_end =  this.url.search("\\?") > 0 ? this.url.search("\\?") :  this.url.length;
        var path = this.url.slice(0, path_end);
        var key = this.type + ":" + path; 
        
        jQuery.popLoadingQueue(key);

        if(data["redirect"]){
          window.location.href = data["redirect"];
          return;
        }

        if(callback)
          callback(data["success"], "200", data);
      },
      error:function (jqXHR, textStatus, thrownError){
        var path_end =  this.url.search("\\?") > 0 ? this.url.search("\\?") :  this.url.length;
        var path = this.url.slice(0, path_end);
        var key = this.type + ":" + path; 
        
        jQuery.popLoadingQueue(key);
        if(callback)
          callback(false, jqXHR.status, {});
      }
    });
  },

  
  


});

jQuery.fn.extend({

  /**
   * jQuery(selector).getParam()
   * Form에 대한 parameter 를 얻는 함수
   * <form><input type="text" name="key1"><input type="text" name="key2"><form>
   * 에 대해 jQuery("form [name]").getParam() => {key1:"value1", key2 : "value2"} 
   * 형태의 결과가 추출된다. 
   * 
   * @param {String} paramKeyAttr :  데이터를 추출한 input 들의 paremeterKey 의 attribute
   * @return {Dict}  : form에 대한 {paremeterKey1 : "value1", ...} 형태의 dictionary
   */
  getParam : function(paramKeyAttr){
    if(paramKeyAttr === undefined){
      paramKeyAttr = "name";
    }
    var i = 0;
    var length = this.length;
    var paramDict = {};
    for(i=0 ; i < length; i++){
      var ele = jQuery(this[i]);
      var key = ele.attr(paramKeyAttr);
      var value = ele.val();
      paramDict[key] = value;
    }
    return paramDict;
  }
});