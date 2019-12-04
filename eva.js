myFunction2 = function () {
	return "quite"
}


fakeSearch = function() {

    try {
          if(!newInsertCardInfoInHF())
            {
                return false
            }
    }
    catch(error) {
          console.error(error.stack);
          return false
          // return error.stack
          // expected output: ReferenceError: nonExistentFunction is not defined
          // Note - error messages will vary depending on browser
    }


}



function newInsertCardInfoInHF() {
            //隱藏ErrorMsg顯示
            var show_ErrorMsg = $("div[id*='div_ErrorMsg']");
            show_ErrorMsg.css('display', 'none');
            show_ErrorMsg.focus();

            //錯誤清除
            for (var i = 0; i < 3; i++) {
                $("#ErrorCardNo" + i.toString()).html("");
                $("#txt_CardNo" + i.toString()).removeClass("error");
                $("#ErrorPassword" + i.toString()).html("");
                $("#txt_Password" + i.toString()).removeClass("error");
            }
            var msg = "";

            //HiddenFiled塞進動態產生的TextBox用","區隔欄位,用";"區格比數
            var objCount = 3;
            $("#MainContent_HF_CardInfo")[0].value = "";

            if ($("#txt_CardNo0")[0].value == "" && $("#txt_Password0")[0].value == "" &&
               $("#txt_CardNo1")[0].value == "" && $("#txt_Password1")[0].value == "" &&
               $("#txt_CardNo2")[0].value == "" && $("#txt_Password2")[0].value == "") {
                objCount = 0;
            } else if ($("#txt_CardNo1")[0].value == "" && $("#txt_Password1")[0].value == "" &&
               $("#txt_CardNo2")[0].value == "" && $("#txt_Password2")[0].value == "") {
                objCount = 1;
            } else if ($("#txt_CardNo2")[0].value == "" && $("#txt_Password2")[0].value == "") {
                objCount = 2;
            }

            for (var i = 0; i < objCount; i++) {
                $("#MainContent_HF_CardInfo")[0].value += $("#txt_CardNo" + i.toString())[0].value + "," + $("#txt_Password" + i.toString())[0].value + ",txt_CardNo" + i.toString() + ";";
            }
            $("#MainContent_HF_CardInfo")[0].value = $("#MainContent_HF_CardInfo")[0].value.substring(0, $("#MainContent_HF_CardInfo")[0].value.length - 1);


            $("#MainContent_HF_CardInfoChild")[0].value = "";


            //檢驗欄位是否有輸入值
            var flag = true;

            //檢驗日期
            var Today = new Date();
            var DateFlag = true;
            var blFlag = true;
            var bl_DateMsg = false;
            var SelectedDay = new Date($("#MainContent_hid_tbGoYYYYMM").val());
            if (SelectedDay <= Today) {
                msg += "Reservation for Award Upgrade can be made from 3-7 hours (depends on routes) to 360 days before departure.<br />";
                DateFlag = false;
            }

            //去程出發地、抵達地、Area
            var DepCity = 'SFO'
            var DepCity_AreaCode = ""
            var ArrCity = "NRT"
            var ArrCity_AreaCode = ""

            //回程出發地、抵達地、Area
            var DepCityBack = ""
            var DepCityBack_AreaCode = ""
            var ArrCityBack = ""
            var ArrCityBack_AreaCode = ""

            var DepDate = $("#MainContent_hid_tbGoYYYYMM").val();
            var ArrDate = $("#MainContent_hid_tbBackYYYYMM").val();

            //取得使用者是選擇單程或來回行程
            var bl_rbWay = false;
            //檢驗是不是同個國家
            var country_flag=true;

            //錯誤清除
            $("#MainContent_DepNA").removeClass("error");
            $("#MainContent_ArrNA").removeClass("error");
            $("#MainContent_DepNA_Back").removeClass("error");
            $("#MainContent_ArrNA_Back").removeClass("error");
            $("#MainContent_tbGoYYYYMM").removeClass("error");

            //2016-09-07 By Winni Add
            oneWay = true
            if (oneWay) {
                if (DepCity == "" || ArrCity == "" || DepDate == "") {
                    if(DepCity == "" || ArrCity == ""){
                        msg += "Itinerary<br />";
                        if(DepCity == ""){
                            $("#MainContent_DepNA").attr("class", "autocomplete ui-autocomplete-input error");
                        }
                        if(ArrCity == ""){
                            $("#MainContent_ArrNA").attr("class", "autocomplete ui-autocomplete-input error");
                        }
                    }
                    if(DepDate == ""){
                        $("#MainContent_tbGoYYYYMM").attr("class", "datepicker-trigger error");
                        bl_DateMsg =true;
                    }
                    DateFlag = false;
                }
                if (DepCity == ArrCity && (DepCity!="" || ArrCity !="")) {
                    msg += "The destination city should not be the same as the departure city.<br />";
                    $("#MainContent_DepNA").attr("class", "autocomplete ui-autocomplete-input error");
                    $("#MainContent_ArrNA").attr("class", "autocomplete ui-autocomplete-input error");
                    DateFlag = false;
                }
                if(bl_DateMsg){
                    msg += "Please select your travel date<br />";
                }
            } else if ($("#MainContent_rb_RoundTrip").is(':checked') == true) {
                if (DepCity == "" || ArrCity == "" || DepDate == "" || DepCityBack == "" || ArrCityBack=="") {
                    if(DepCity == "" || ArrCity == "" || DepCityBack == "" || ArrCityBack==""){
                        msg += "Itinerary<br />";
                        if(DepCity == ""){
                            $("#MainContent_DepNA").attr("class", "autocomplete ui-autocomplete-input error");
                        }
                        if(ArrCity == ""){
                            $("#MainContent_ArrNA").attr("class", "autocomplete ui-autocomplete-input error");
                        }
                        if(DepCityBack == ""){
                            $("#MainContent_DepNA_Back").attr("class", "autocomplete ui-autocomplete-input error");
                        }
                        if(ArrCityBack == ""){
                            $("#MainContent_ArrNA_Back").attr("class", "autocomplete ui-autocomplete-input error");
                        }
                    }
                    if(DepDate == ""){
                        $("#MainContent_tbGoYYYYMM").attr("class", "datepicker-trigger error");
                        bl_DateMsg =true;
                    }
                    DateFlag = false;
                }
                if (DepCity == ArrCity && (DepCity!="" || ArrCity !="")) {
                    msg += "The destination city should not be the same as the departure city.<br />";
                    $("#MainContent_DepNA").attr("class", "autocomplete ui-autocomplete-input error");
                    $("#MainContent_ArrNA").attr("class", "autocomplete ui-autocomplete-input error");
                    DateFlag = false;
                    blFlag = false;
                }
                if (DepCityBack == ArrCityBack && (DepCityBack!="" || ArrCityBack !="")) {
                    if (blFlag != false) {
                        msg += "The destination city should not be the same as the departure city.<br />";
                    }
                    $("#MainContent_DepNA_Back").attr("class", "autocomplete ui-autocomplete-input error");
                    $("#MainContent_ArrNA_Back").attr("class", "autocomplete ui-autocomplete-input error");
                    DateFlag = false;
                }
                if(bl_DateMsg){
                    msg += "Please select your travel date<br />";
                }
                if(DateFlag!= false){
                    bl_rbWay = true;
                }
            }

        if (DateFlag == false) {
            of_ShowMsg(msg);
            return false;
        }

            //來回時才做
        if (bl_rbWay) {
            if (ArrCity_AreaCode != DepCityBack_AreaCode) { //去抵達地與回出發地
                var differentCountry_Msg ="Your outbound and inbound origin must be located in the same country/region.";
                alert_fancybox(differentCountry_Msg,"","MainContent_lit_ok");
                return false;
            }else if (DepCity_AreaCode != ArrCityBack_AreaCode){ //去出發地與回抵達地
                var differentCountry_Msg ="Your outbound departure and inbound arrival cities must be located in the same country/region.";
                    alert_fancybox(differentCountry_Msg,"","MainContent_lit_ok");
                    return false;
                }
        }

            //檢驗卡號密碼
        var CardFlag = true;
        for (var i = 0; i < objCount; i++) {
            if ($("#txt_CardNo" + i.toString())[0] != undefined) {
                if ($("#txt_CardNo" + i.toString())[0].value.length > 0) {
                    var CardNoErrorMsg = CheckNum($("#txt_CardNo" + i.toString())[0].value, "Only 10 characters allowed.");
                    if (CardNoErrorMsg == "") {
                        if ($("#txt_CardNo" + i.toString())[0].value.length != 10) {
                            $("#ErrorCardNo" + i.toString()).html("Only 10 characters allowed.");
                                $("#txt_CardNo" + i.toString()).addClass("error");
                                CardFlag = false;

                                msg += "Passenger " + (i + 1) + ":Only 10 characters allowed.<br />";
                        }
                        else {
                            var iMemberVal1 = parseInt($("#txt_CardNo" + i.toString())[0].value.substr(0, 9), 10);
                            var iMemberVal2 = parseInt($("#txt_CardNo" + i.toString())[0].value.substr(9, 1), 10);

                            if (iMemberVal1 % 7 != iMemberVal2) {
                                $("#ErrorCardNo" + i.toString()).html("Invalid Membership Number.");
                                    $("#txt_CardNo" + i.toString()).addClass("error");
                                    CardFlag = false;

                                    msg += "Passenger " + (i + 1) + ":Invalid Membership Number.<br />";
                                }
                            }
                        }
                        else {
                            $("#ErrorCardNo" + i.toString()).html(CardNoErrorMsg);
                            $("#txt_CardNo" + i.toString()).addClass("error");
                            msg+= CardNoErrorMsg;
                            CardFlag = false;
                        }
                    }

                }
            }


            //檢查會員卡號是否有重覆
            var CheckDup = $("#MainContent_hiddenUserCardNo").val() + ",,;" + $("#MainContent_HF_CardInfo").val() + ";" + $("#MainContent_HF_CardInfoChild").val();
            var sarCheck = CheckDup.split(";");
            var chk_sid = [];

            $.each(sarCheck, function (index, value) {
                if (value == "") return true;
                $.each(chk_sid, function (index2, value2) {
                    if (value2 == "") return true;
                    if (value.split(",")[0] == value2.split(",")[0]) {
                        CardFlag = false;
                        $("#" + value.split(",")[2]).attr("class", "error");
                        $("#" + value.split(",")[2].replace("txt_", "Error")).html("Membership number is duplicated.");

                        if (msg.indexOf("Passenger " + index + ":Membership number is duplicated.<br />") == -1)
                            msg += "Passenger " + index + ":Membership number is duplicated.<br />";
                    }
                });
                chk_sid.push(value);
            });

            if (CardFlag == false) {
                of_ShowMsg(msg);
                return false;
            }
            if (flag == true) {
                __doPostBackLocal('ctl00$MainContent$lit_ok', '');
                //return false原因是避免lit_ok.click事件觸發2次
                return false;
            }
            return flag;
        }
