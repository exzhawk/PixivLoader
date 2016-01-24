// Generated by CoffeeScript 1.10.0
(function() {
  $(function() {
    var $big, $thumbnail, change_to, current_page;
    $big = $('#big');
    $thumbnail = $('#thumbnail');
    $thumbnail.owlCarousel({
      items: 5,
      margin: 10,
      center: true,
      nav: false,
      dots: false
    }).on('mousewheel', function(e) {
      if (e.deltaY < 0) {
        $thumbnail.trigger('next.owl');
      } else {
        $thumbnail.trigger('prev.owl');
      }
      return e.preventDefault();
    }).on('click', '.owl-item', function(e) {
      e.preventDefault();
      return $thumbnail.trigger('to.owl.carousel', [$(this).index(), 250, true]);
    }).on('changed.owl.carousel', function(e) {
      var current;
      current = e.item.index;
      return change_to(current);
    });
    change_to = function(index) {
      var img_src;
      img_src = $thumbnail.find('.owl-stage').children('.owl-item').eq(index).find('.thumbnail_img').attr('big');
      return $big.css("background-image", "url('/get_file/" + img_src + "')");
    };
    $('#nextBtn').on("click", function() {
      return $thumbnail.trigger("next.owl");
    });
    $('#prevBtn').on("click", function() {
      return $thumbnail.trigger("prev.owl");
    });
    current_page = 1;
    return $.getJSON({
      url: '/get_following/' + current_page,
      success: function(data) {
        var $item, i, illust, len;
        for (i = 0, len = data.length; i < len; i++) {
          illust = data[i];
          if (illust['special'] !== 'ugoku') {
            $item = $('<div>').addClass('owl-item');
            $('<div>').addClass('thumbnail_img').attr('big', illust['img'][0]).css("background-image", "url('/get_file/" + illust['thumbnail'] + "')").appendTo($item);
            $thumbnail.trigger("add.owl.carousel", [$item]);
          }
        }
        $thumbnail.trigger("refresh.owl.carousel");
        return change_to(0);
      }
    });
  });

}).call(this);

//# sourceMappingURL=app.js.map
