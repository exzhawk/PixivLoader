$ ->
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

  $('#nextBtn').on "click", ->
    $thumbnail.trigger "next.owl"
  $('#prevBtn').on "click", ->
    $thumbnail.trigger "prev.owl"

#  current_page=1
#  $.getJSON
#    url:'/get_following/'+current_page
#    success:(data)->
#      for illust in data
#        if illust['special']
#          $thumbnail.trigger()
#          todo add item


