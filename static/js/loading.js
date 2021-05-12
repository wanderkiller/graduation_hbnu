//如果把这段注释掉，会一直停留在加载的页面上
$(window).load(function(){
             $(".loading").fadeOut()
        })

// 页面自适应
$(document).ready(
function()
    {
        var whei=$(window).width()
        $("html").css({fontSize:whei/20})

        $(window).resize(
        function()
            {
            var whei=$(window).width()
            $("html").css({fontSize:whei/20})
            }
        );

	}
);