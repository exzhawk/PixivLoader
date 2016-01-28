$ ->
  init = true
  $big = $('#big')
  $thumbnail = $('#thumbnail')
  $thumbnail
  .owlCarousel
      items: 5
      margin: 10
      center: true
      nav: false
      dots: false
  .on 'mousewheel', (e)->
    if e.deltaY < 0
      $thumbnail.trigger 'next.owl'
    else
      $thumbnail.trigger 'prev.owl'
    e.preventDefault()
  .on 'click', '.owl-item', (e)->
    e.preventDefault()
    $thumbnail.trigger 'to.owl.carousel', [$(this).index(), 250, true]
  .on 'changed.owl.carousel', (e) ->
    current = e.item.index
    change_to(current)
    count = e.item.count
    if count - current == 1
      load_page(current_page)


  change_to = (index) ->
    img = $thumbnail.find('.owl-stage').children('.owl-item').eq(index).find('.thumbnail_img')
    img_src = img.attr 'big'
    $big.css("background-image", "url('/get_file/" + img_src + "')")
    title = img.attr 'title'
    $("#title").text(title)
    author_name = img.attr 'author_name'
    $("#author").text(author_name)


  $('#nextBtn').on "click", ->
    $thumbnail.trigger "next.owl"
  $('#prevBtn').on "click", ->
    $thumbnail.trigger "prev.owl"

  load_page = (page_number) ->
    $.getJSON
      url: '/get_following/' + page_number
      success: (data)->
        for illust in data
          if illust['special'] != 'ugoku'
            $item = $('<div>')
            .addClass 'owl-item'
            $('<div>')
            .addClass 'thumbnail_img'
            .attr 'big', illust['img'][0]
            .attr 'title', illust['title']
            .attr 'author_name', illust['author_name']
            .css("background-image", "url('/get_file/" + illust['thumbnail'] + "')")
            .appendTo($item)
            $thumbnail.trigger "add.owl.carousel", [$item]
        $thumbnail.trigger "refresh.owl.carousel"
        console.log(init)
        if init == true
          change_to(0)
          init = false
    current_page += 1


  current_page = 1
  load_page(current_page)

