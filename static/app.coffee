$ ->
  $thumbnail = $('#thumbnail')
  $thumbnail
  .owlCarousel
      items: 5
      margin: 10
      center: true
      nav: false
      dots: false
  .on 'mousewheel', '.owl-stage', (e)->
    if e.deltaY < 0
      $thumbnail.trigger 'next.owl'
    else
      $thumbnail.trigger 'prev.owl'
    e.preventDefault()

  $('#nextBtn').on "click", ->
    $thumbnail.trigger "next.owl"
  $('#prevBtn').on "click", ->
    $thumbnail.trigger "prev.owl"



