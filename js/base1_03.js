var PROGRE = PROGRE || {};
PROGRE.util = {
  strip: function(a) {
    return a.replace(/^\s*(.*?)\s*$/, "$1")
  }
};

PROGRE.app = {
  setupFbBtn: function() {
    var a = [];
    a.push("//www.facebook.com/plugins/like.php?href=" + document.URL);
    a.push("&send=false&layout=button_count&width=100&show_faces=false&action=like&colorscheme=light&font&height=21&appId=377916442224535");
    a = a.join("");
    var b = '<iframe src="' + a + '" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:100px; height:21px;" allowTransparency="true"></iframe>';
    $("#fb-button").append(b)
  }
};

$(function(){
	// set up fb like
	var src  = [];
	src.push('//www.facebook.com/plugins/like.php?href=' + document.URL);
	src.push('&amp;send=false&amp;layout=button_count&amp;width=100&amp;show_faces=false&amp;action=recommend&amp;colorscheme=light&amp;font&amp;height=21&amp;appId=377916442224535');
	src = src.join('');
	var html = '<iframe src="' + src + '" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:100px; height:21px;" allowTransparency="true"></iframe>';
	$("#fb-button").append(html);
	
    // click content
    $(".list-name").click(function(){
    	if ($(this).next(".second-list").hasClass("closed-list")) {
    		$(this).nextAll(".second-list").removeClass("closed-list");
            $(this).parent("ul").find(".band-name-list").slideDown('fast');
    	} else {
    		$(this).nextAll(".second-list").addClass("closed-list");
            $(this).parent("ul").find(".band-name-list").slideUp('fast');
    	}
    });

    // click genre
    $(".genre-name").click(function(){
    	if ($(this).parent(".second-list").hasClass("closed-list")) {
    		$(this).parent(".second-list").removeClass("closed-list");
    	} else {
    		$(this).parent(".second-list").addClass("closed-list");
    	}
        $(this).next(".band-name-list").slideToggle('fast');
    });

    // band hover
    $(".band-name-list > li").hover(
    	function(){
    		$(this).addClass("selected");
    	},
    	function(){
    		$(this).removeClass("selected");
    	}
    );

    // mail
    var mailto = "mailto:";
    var madrs = "info";
	var domain = "progre-meiban.com";
	var madrs = madrs + unescape("%40") + domain;
	$(".mail-address").attr("href",mailto + madrs).append(madrs)
	
	// amazon-mp3による試聴の案内
	var shichou = "↓試聴できます↓";
	$(".amazon-mp3").prepend("<p>" + shichou + "</p>");

	// back
	$("#parent-url").click(
    	function() {
    		if (document.referrer.match(/http:\/\/progre-meiban\.com/)) {
    			history.back();
    		} else {
	    		var current_url = document.URL;
		    	var last_slash = current_url.lastIndexOf("/");
		    	var parent_url = current_url.substring(0, last_slash) + ".shtml";
		    	location.href = parent_url;
    		}
	    }
	);

	// color changer
	var path_arr = document.URL.split('/');
	path_arr.shift();
	path_arr.shift();
	path_arr.shift();
	path_arr.shift();
	var link;
	while(path_arr.length){
		link=$('#navi').find('a[href*="/'+path_arr.join('/')+'"]');
		if(link.length){
			link.parent("li").addClass("fix-selected");
			// 親要素のsecond-list以外はリストを閉じる
			$('#navi').find('.second-list')
                .not('.special-list')
                .not(":has('.fix-selected')")
                .addClass("closed-list")
                .children(".band-name-list")
                .slideToggle('fast');
            break;
		}
	path_arr.pop();
	}

	// hover
    $(".column > li > a, .child-column > li >a ").hover(
    	function(){
    		$(this).css("text-decoration", "underline")
    	},
    	function(){
    		$(this).css("text-decoration", "none");
    	}
    );

    // bread crumbs
    $('#breadcrumbs').xBreadcrumbs();
    // ドメイン名を除いたURLを抽出する
    fileName = document.URL.substring(document.URL.indexOf("/", 8), document.URL.length)
    $('#breadcrumbs').children('li').children('a[href$="' + fileName + '"]').parent('li').attr('class', 'current')

    // comment form
    var isMSIE = /*@cc_on!@*/false;
    if (isMSIE) {
        $('#slideout').remove();
    } else {
        $('#slideout').css('visibility', 'visible');
        // コメント送信フォーム
        $('#comment_form').submit(function() {
            // ボタンを非活性化
            $("#mail-send-button").attr("disabled", "disabled");
            // クエリ
            var query = $("#comment_form").serialize();
            console.log(query);
            // POSTリクエスト
            $.post("/cgi/sendmail.py", query, function(value){
                alert('ありがとうございます！！');
                console.log('return value is ' + String(value))
            });
        });
    }
});

// analytics
var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-21607493-2']);
_gaq.push(['_trackPageview']);

(function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();

