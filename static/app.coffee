$ ->
  init = true
  loading = false
  $big = $('#big')
  $$big = $big[0]
  $thumbnail = $('#thumbnail')
  $thumbnail
  .owlCarousel
      center: true
      nav: false
      dots: false
      responsive:
        0:
          items: 5
        1200:
          items: 9
        1800:
          items: 13
  .on 'mousewheel', (e)->
    if e.deltaY < 0
      $thumbnail.trigger 'next.owl'
    else
      $thumbnail.trigger 'prev.owl'
    e.preventDefault()
  .on 'click', '.owl-item', (e)->
    e.preventDefault()
    $thumbnail.trigger 'to.owl.carousel', [$(this).index(), 200, true]
  .on 'changed.owl.carousel', (e) ->
    current = e.item.index
    change_to(current)
    count = e.item.count
    if count - current < 20
      if loading == false
        loading = true
        load_page(current_page)

  $('#open_touch').on 'mousewheel', (e)->
    if e.deltaY < 0
      $$big.next_pic()
    else
      $$big.prev_pic()
    e.preventDefault()

  $$big.next_pic = ->
    if $$big.img_data['is_manga']
      if $$big.current_page < $$big.total_page
        $$big.current_page += 1
        set_big_background_to_page($$big.current_page)

  $$big.prev_pic = ->
    if $$big.img_data['is_manga']
      if $$big.current_page > 0
        $$big.current_page -= 1
        set_big_background_to_page($$big.current_page)


  change_to = (index) ->
    img_data = $thumbnail.find('.owl-stage').children('.owl-item').eq(index).find('.thumbnail_img')[0].img_data
    $$big.img_data = img_data
    $('#caption').text img_data['caption']
    $('#title')
    .text img_data['title']
    .attr 'href', 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + img_data['id']
    $('#author')
    .text img_data['user']['name']
    .attr 'href', 'http://www.pixiv.net/member_illust.php?id=' + img_data['user']['id']
    if img_data['is_manga']
      $$big.pages = img_data['metadata']['pages']
      $$big.total_page = $$big.pages.length - 1
      $$big.current_page = 0
      set_big_background_to_page($$big.current_page)
    else if img_data['type'] == 'ugoira'
      $$big.zip_urls = img_data['metadata']['zip_urls']['ugoira600x600']
      $$big.frames = img_data['metadata']['frames']
    else
      $big.css 'background-image', encode_css_background_image_url(img_data['image_urls']['large'])

  set_big_background_to_page = (page_number) ->
    $big.css 'background-image', encode_css_background_image_url($$big.pages[page_number]['image_urls']['large'])

  encode_css_background_image_url = (url) ->
    'url("/get_file/' + encodeURIComponent(url) + '")'

  $('#prev_touch').on "click", (e) ->
    $thumbnail.trigger "prev.owl"
    e.preventDefault()
  $('#next_touch').on "click", (e)->
    $thumbnail.trigger "next.owl"
    e.preventDefault()

  load_page = (page_number) ->
    $.getJSON
      url: '/get_following/' + page_number
      success: (data)->
        for illust in data
          $img = $('<div>')
          .addClass 'thumbnail_img'
          .css 'background-image', encode_css_background_image_url(illust['image_urls']['small'])
          $img[0].img_data = illust
          if illust['is_manga']
            $img.addClass('multi')
          else if illust['type'] == 'ugoira'
            $img.addClass('ugoira')
          else
            $img.addClass('illust')
          $item = $('<div>').addClass('owl-item').append($img)
          $thumbnail.trigger "add.owl.carousel", [$item]
        $thumbnail.trigger "refresh.owl.carousel"
        if init == true
          change_to(0)
          init = false
        loading = false
    current_page += 1


  $(document).on 'keydown', (e) ->
    switch e.which
      when 33 #pgup
        shown_count = $('.owl-stage .active').length + 1
        current_page = $('.owl-stage .center').index('.owl-stage > .owl-item')
        $thumbnail.trigger 'to.owl.carousel', [current_page - shown_count, 200, true]
      when 34 #pgdn
        shown_count = $('.owl-stage .active').length + 1
        current_page = $('.owl-stage .center').index('.owl-stage > .owl-item')
        $thumbnail.trigger 'to.owl.carousel', [current_page + shown_count, 200, true]
      when 35 #end
        total_count = $('.owl-stage > .owl-item').length
        $thumbnail.trigger 'to.owl.carousel', [total_count - 1, 200, true]
      when 36 #home
        $thumbnail.trigger 'to.owl.carousel', [0, 200, true]
      when 37 #left
        $thumbnail.trigger 'prev.owl'
      when 38 #up
        $$big.prev_pic()
      when 39 #right
        $thumbnail.trigger 'next.owl'
      when 40 #down
        $$big.next_pic()


  current_page = 1
  load_page(current_page)

