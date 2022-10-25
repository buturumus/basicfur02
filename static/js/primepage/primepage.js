// primepage/primapage.js

'use strict';

// some global vars
//let activeTabheaderLink = '';

let currTabName; 
let parentTabName = '';
let htmlBody; // sometimes should be global
// flags for yes/no page
let isYesNoActive = false;
let isYesNoPassed = false;
let isYesPressed = false;

const SPINNER_HTML=`
<p></p>
<div class="spinner-cont text-center">
  <div class="spinner-border role="status">
    <span class="sr-only">
      Loading...
    </span>
  </div>
</div>
<p></p>
`


/* Common functions */


// multiclass inheritance crutch
function Classes(...baseClasses) {
  // no need to call super() for child constructor

  class ResultClass {
    constructor() {
      baseClasses.forEach(
        baseClass => Object.assign(this, new baseClass())
      );
    }
  }

  baseClasses.forEach(baseClass => {
    Object.getOwnPropertyNames(baseClass.prototype)
    .filter(prop => prop != 'constructor')
    .forEach(
      prop => ResultClass.prototype[prop] = baseClass.prototype[prop]
    )
  })
  return ResultClass;
}


/* old */


function getValOrText(field) {
  let val;
  val = $(field).val();
  // if empty val() try to get text() instead
  if( !(val) && typeof( $(field).text() != 'undefined') )
    val = $(field).text().trim();
  return val;
}


function getIdFromDropdown(dropdown) {
  if($(dropdown).val())
    for(const option of dropdown.find('option') ) {
      if( option.value == $(dropdown).val() )
        return $(option).attr('shadow_id');
    }
  ;
  return '';
}


// for csrf protection
function getCookie(CName) {
  if (document.cookie.length > 0) {
    let CStart = document.cookie.indexOf(CName + '=');
    if (CStart != -1) {
      CStart = CStart + CName.length + 1;
      let CEnd = document.cookie.indexOf(';', CStart);
      if (CEnd == -1) CEnd = document.cookie.length;
      return unescape(document.cookie.substring(CStart,CEnd));
    }
  }
  return '';
}


function sendAjaxPost(addr, objToSend, funcOnAjaxSuccess) {
  // preprocessor for array of arrays
  for (const theKey in objToSend) {
    if (objToSend[theKey] instanceof Array) 
      objToSend[theKey] = JSON.stringify(objToSend[theKey]);
  };
  $.ajax({
    type:         'POST',
    headers:      {"X-CSRFToken":   getCookie('csrftoken') },
    url:          addr,
    data:         objToSend,
    cache:        false,
    success:      funcOnAjaxSuccess,  // it's arg = response data
    dataType:     'json',
  })
}


function loadTabPart(
  url,
  request, 
  objToAppendTo, 
  callback = () => {} 
){ 
  sendAjaxGet_(url, request, function(jsonData){ 
    objToAppendTo.append(jsonData);
    /*
    // get html response
    htmlBody = jsonData['html_in_json'];
    // append tab's part to it's container
    objToAppendTo.append(htmlBody);
    // look for js to run on load and run it
    const addedJqueryHeader = $(objToAppendTo).find(
        '[tab_action="' + request['tab_action'] + '"]'
        + '[matrix_type="' + request['matrix_type'] + '"]'
        + '[tab_model="' + request['tab_model'] + '"]'
    );
    const funcNames = $(addedJqueryHeader).attr('run_on_load');
    if(typeof funcNames !== 'undefined') {
      funcNames.split(' ').forEach(
        (funcName) => { 
          // run if func exists
          if(jsFuncs[funcName]) {
            jsFuncs[funcName](addedJqueryHeader); 
          };
        }
      )
    };
    // after the download
    callback();
    */
  });
}


/* Classes */


class PagepartGetter {

  constructor(){
    this.tabCmd = '';
    this.url = '';
    this.objToSend = {};
    this.objToAppendTo = {};
    this.funcOnAjaxSuccess = () => {};
  }

  sendAjaxGet() {
    $.ajax({
      type:         'GET',
      url:          this.url,
      data:         this.objToSend,
      cache:        false,
      success:      this.funcOnAjaxSuccess,  // it's arg = response
      dataType:     'html',
    })
  }

}


class ShownMatrixGetter extends PagepartGetter {

  constructor(parentBodieGetter){
    super();
    this.objToAppendTo = $(
      '#tab-bodies-cont ' 
      + `.tab-bodie[tab_cmd=${parentBodieGetter.tabCmd}] `
      + '.tab-matrix-cont'
    );
    this.tabCmd = parentBodieGetter.tabCmd;
    this.pk = parentBodieGetter.pk;
    this.url = `/part/${this.tabCmd}/matrix/${this.pk}/`;
    this.funcOnAjaxSuccess = (resp) => { 
      // wipe wheel
      this.objToAppendTo.children().remove();
      // put downloaded content to it's place
      const addedMatrix = this.objToAppendTo.append(resp)
        .children(':last-child');
      // and activate pensils
      addedMatrix.find('.pensil').click(function() {
        // check to avoid duplication 
        const existBodie = $('#tab-bodies-cont')
          .find(`.tab-bodie[uniq_category=${$(this).attr('uniq_category')}]`);
        const uniqCategory = $(existBodie).attr('uniq_category');
        if ( ! uniqCategory) {
          // add if such tab doesn't exists 
          const clickProcessor = new PensilClickProcessor(this);
          clickProcessor.sendAjaxGet();
        } else {
          // or activate existing
          $(`#tab-header-link-${uniqCategory}`).tab('show');
        };
      });
    };
  }

  activatePensils(theMatrix) {
    $(document).find('.pensil').click(function() {
      // check to avoid duplication 
      const existBodie = $('#tab-bodies-cont')
        .find(`.tab-bodie[uniq_category=${$(this).attr('uniq_category')}]`)
      const uniqCategory = existBodie.attr('uniq_category');
      if ( ! uniqCategory) {
        // add if such tab doesn't exists 
        const clickProcessor = new SidebarClickProcessor(this);
        clickProcessor.sendAjaxGet()
      } else {
        // or activate existing
        $(`#tab-header-link-${uniqCategory}`).tab('show');
      };
    });
  }

}


class ShownTabheaderGetter extends PagepartGetter {

  constructor(parentBodieGetter){
    super();
    this.objToAppendTo = $('#tab-headers-cont');
    this.tabCmd = parentBodieGetter.tabCmd;
    this.pk = parentBodieGetter.pk;
    this.url = `/part/${this.tabCmd}/tabheader/${this.pk}/`,
    this.funcOnAjaxSuccess = (resp) => { 
      // put downloaded content to it's place
      const addedTabheader = this.objToAppendTo.append(resp)
        .children(':last-child');
      // activate the tabheader, mandatory
      addedTabheader.find('.tab-header-link').tab('show');
      // show wheel
      $('#tab-bodies-cont '
        + `.tab-bodie[tab_cmd=${parentBodieGetter.tabCmd}] `
        + '.tab-matrix-cont'
      ).append(SPINNER_HTML);
      // load matrix
      const matrixGetter = new ShownMatrixGetter(parentBodieGetter);
      matrixGetter.sendAjaxGet();
    };
  }

}


class ShownBodieGetter extends PagepartGetter {

  constructor(){
    super();
    this.objToAppendTo = $('#tab-bodies-cont');
  }

  activateRefreshButton(tabBodie) {
    const currentBodieGetter  = this
    tabBodie.find('.refresh-btn').click(function() {
      // delete matrix
      $(tabBodie).find('.scrollbarable').remove();
      // show wheel
      $('#tab-bodies-cont '
        + `.tab-bodie[tab_cmd=${currentBodieGetter.tabCmd}] `
        + '.tab-matrix-cont'
      ).append(SPINNER_HTML);
      // load matrix again
      const matrixGetter = new ShownMatrixGetter(currentBodieGetter);
      matrixGetter.sendAjaxGet();
    });
  } 

  activateCloseButton(tabBodie) {
    tabBodie.find('.close-btn').click(function() {
      /* 
        bootstrap's tab header consists of
        tab header's container(li) and child tab header's link(a)
        which points to tab's body(tab frame in our case and terms)
      */
      const tabheaderLinkToClose = $(
        '.tab-header-link[href="#' + $(tabBodie).attr('id') + '"]'
      ).parent();
      // find out who'll be the next
      let newTabheaderLink = '';
      if ($(tabheaderLinkToClose).next().attr('id')) {
        newTabheaderLink = $(tabheaderLinkToClose).next();
      } else if ($(tabheaderLinkToClose).prev().attr('id')) {
        newTabheaderLink = $(tabheaderLinkToClose).prev();
      };
      // remove old
      $(tabheaderLinkToClose).remove();
      $(tabBodie).remove();
      // show new
      if (newTabheaderLink) { 
        $(newTabheaderLink).children('a').first().tab('show');
      };
    })
  }

  activateButtons(parentCont) {
    this.activateRefreshButton(parentCont);
    this.activateCloseButton(parentCont);
  } 

}


class PensilClickProcessor extends ShownBodieGetter {

  constructor(clickableItem){
    super();
    this.tabCmd = $(clickableItem).attr('tab_cmd');
    this.pk = $(clickableItem).closest('tr[pk]').attr('pk');
    this.url = `/part/${this.tabCmd}/bodie/${this.pk}/`;
    // ajax callback: add downloaded content to the tab bodie.
    this.funcOnAjaxSuccess = (resp) => { 
      const addedBodie = this.objToAppendTo.append(resp)
        .children(':last-child');
      this.activateButtons(addedBodie);
      // load header(then bodie etc.)
      const tabheaderGetter = new ShownTabheaderGetter(this);
      tabheaderGetter.sendAjaxGet();
    };
  }

}


class SidebarClickProcessor extends ShownBodieGetter {

  constructor(clickableItem){
    super();
    this.tabCmd = $(clickableItem).attr('tab_cmd');
    this.pk = 0;  // for all sidebar clickables
    this.url = `/part/${this.tabCmd}/bodie/${this.pk}/`;
    // ajax callback: add downloaded content to the tab bodie.
    this.funcOnAjaxSuccess = (resp) => { 
      const addedBodie = this.objToAppendTo.append(resp)
        .children(':last-child');
      this.activateButtons(addedBodie);
      // load header(then bodie etc.)
      const tabheaderGetter = new ShownTabheaderGetter(this);
      tabheaderGetter.sendAjaxGet();
    };
  }

}


/* Main entry point: activate sidebar clickable items */


$(document).ready(function() {
  $(document).find('.click-for-tab').click(function() {
    // check to avoid duplication 
    const existBodie = $('#tab-bodies-cont')
      .find(`.tab-bodie[uniq_category=${$(this).attr('uniq_category')}]`)
    const uniqCategory = existBodie.attr('uniq_category');
    if ( ! uniqCategory) {
      // add if such tab doesn't exists 
      const clickProcessor = new SidebarClickProcessor(this);
      clickProcessor.sendAjaxGet()
    } else {
      // or activate existing
      $(`#tab-header-link-${uniqCategory}`).tab('show');
    };
  });
});

