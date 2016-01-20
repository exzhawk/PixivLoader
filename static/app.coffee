$ ->
  $big = $('#big')
  $small = $('#small')

  $big.owlCarousel
    singleItem: true
    slideSpeed: 1000
    navigation: true
    pagination: false
    afterAction: syncPosition
    responsiveRefreshRate: 500

  $small
  .owlCarousel
      items: 15
      itemsDesktop: [1119, 10]
      itemsDesktopSmall: [979, 10]
      itemsTablet: [768, 8]
      itemsMobile: [479, 4]
      pagination: false
      responsiveRefreshRate: 500
      afterInit: (el)->
        el.find(".owl-item").eq(0).addClass("synced")
  .on "click", ".owl-item", (e) ->
    e.preventDefault()
    number = $(this).data("owlItem")
    $big.trigger "owl.goTo", number

  syncPosition = (el) ->
    current = this.currentItem
    $small
    .find ".owl-item"
    .removeClass "synced"
    .eq current
    .addClass "synced"
    if $small.data("owlCarousel") != undefined
      center current

  center = (number) ->
    sync2visible = $small.data("owlCarousel").owl.visibleItems
    num = number
    found = false
    for i of sync2visible
      if num == sync2visible[i]
        found = true
    if found == false
      if num > sync2visible[sync2visible.length - 1]
        $small.trigger "owl.goTo", num - sync2visible.length + 2
      else
        if num - 1 == -1
          num = 0
        $small.trigger "owl.goTo", num
    else if num == sync2visible[sync2visible.length - 1]
      $small.trigger "owl.goTo", sync2visible[1]
    else if num == sync2visible[0]
      $small.trigger "owl.goTo", num - 1
