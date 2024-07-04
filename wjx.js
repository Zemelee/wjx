// ==UserScript==
// @name         问卷星脚本
// @author       钟天宇
// @version      7.0
// @description  使用教程：https://www.bilibili.com/video/BV19c411w7qK;一个可以代刷问卷的网站：sugarblack.top/dist;有疑问请加qq群咨询：774326264 || 427847187 || 850281779；不要因为安装量少就不安装啊！我是23年5月新出的脚本，而且还在不断更新中！（2023.8.27）作者很自信这是GF网站上最好用的脚本之一
// @match        *://*.wjx.*
// @match        https://www.wjx.cn/*
// @match        https://w.wjx.com/*
// @match        https://v.wjx.cn/*
// @require      https://cdnjs.cloudflare.com/ajax/libs/localforage/1.7.3/localforage.min.js
// @namespace    https://greasyfork.org/users/1079332
// ==/UserScript==
 
localStorage.clear();
sessionStorage.clear();
console.log("Storage已清除!")
localforage.config({  //左边的黄色警告不用管
    driver: localforage.INDEXEDDB,
    name: 'wjx'  //准备 wjx 数据库
});
//左边的黄色警告不用管，只要不是红色就不影响运行
localforage.getItem("wjx_count").then(value => {
    if (value !== null) {
        QDPOYIt1();
    } else {
        return localforage.setItem("wjx_count", 0).then(() => {
            QDPOYIt1();
        });
    }
}).catch(() => {
    console.log("如果自动刷新多次仍不能提交成功，可手动刷新干预")
});
 
var cancelBtn = document.querySelector('a.layui-layer-btn1');
if (cancelBtn) {
    cancelBtn.click();
}
 
(async function () {
    //将下面的链接替换成你的问卷链接，谁要把vm改成vj我杀了他啊啊啊啊
    var url = "https://www.wjx.cn/vm/hxxt2Oe.aspx";
    // 若当前页面为问卷调查完成页，重定向到目标 URL
    if (window.location.href.includes("join")) {
        setCount();
        window.location.href = url;
    }
    var opt;
    //在单选题的函数single()中，括号里需要写题号和每个选项的比例，比如single(1, [1,2,3])表示第1题，选A占1/(1+2+3),B占2/6,C占3/6;
    //单选：也可以写成百分比的形式，比如[1,20,79],毕竟百分比也是比例；选项数量和比例数量必须一致，否则会报错
    //在多选题的函数multiple()，括号里需写题号和各选项选择的人数比，比如multiple(2, [50,10,100])表示第2题，选A的人有50%,选B的人有10%,选C的人有100%;、
    //多选：每个选项的概率彼此独立,不需要让概率和加起来等于100，
    //在填空题的函数vacant()中,括号里需写题号，内容和每个内容对应的比例，比如vacant(3,[1,1],["hello","world"])表示第3题，填写hello和world的比例为1: 1
    //nextPage()表示翻页
    //{"1": [1, 0, 0, 0, 0],.......}表示矩阵题各个小题的比例，其中的每个小题概率含义与单选题一致
    //在矩阵题的函数matrix()中，括号里需要写题号和每个选项的比例，比如matrix(4,{...})表示第4题，每个小题按照中括号里写的比例刷数据
    //在单选题的函数scale()中，括号里需要写题号和每个选项的比例，比如scale(5,[1,1,2,2,6])表示第5题，A:B:C:D:E = 1:1:2:2:6(和单选题意思一致)
    //在滑块题的函数slide()中,括号里需写题号,以及希望分数最大最小值，slide(7,50,70)表示第7题，分数介于50和70之间
    //所有输入，请在英文输入法里进行，中文和英文的很多符号是不一样的，比如---->    （）()  ｛｝{}   ：:   ,， ;；
 
 
 
 
    //目前脚本可以处理单选（single）、多选（multiple）、矩阵（matrix）、滑块（slide）、填空（vacant）、量表（scale）类问题，这也包括了大部分常见题型
    //下面是需要修改的代码，注意注意，刷完后为了躲避检测我故意让停留了10秒再提交
    //所以选完后10秒内不会有任何反应，这是正常情况！啊当然如果你等了好几十秒了都还没反应的话，可能就是报错了哈哈，这个时候你可以进群咨询哦~~~（2023-05-28）
    //进群若需提问，先看群公告，提问前先学会提问。
    //所有刷问卷的教程都只能让问卷数据总体表面上看起来合理，并不一定保证信效度；
    //如果对信效度有要求，可以找作者代刷，作者在群里;作者现在也是个眼神充满清澈愚蠢的大学生。也是曾经被问卷折磨才诞生了此脚本（2023-12-06）
    //  有一个很好用的刷问卷的网站：sugarblack.top/dist,由我开发的yahoo~
 
    single(1, [1, 2, 3]) //题型(题号，[比例]) | 一行只写一个题的代码 | 比例和选项个数必须一致
    multiple(2, [50, 10, 100])
    vacant(3, ["hello", "world", "!"], [1, 1, 2])
    nextPage();
    matrix(4, { "1": [1, 0, 0, 0, 0], "2": [1, 1, 1, 1, 1], "3": [1, 0, 0, 0, 0], "4": [1, 0, 0, 0, 0] })
    scale(5, [1, 1, 2, 2, 6])
    scale(6, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    slide(7, 50, 70)
    opt = single(8, [1, 1])  //opt只支持single和scale，暂不支持其他类型
    if (opt == 1) {
        single(9, [1, 1])
    }
    single(10, [2, 1])
 
    await reorder(11) //排序题函数，只需要传 题号(11) 参数即可；同时在函数前加一个await和空格
    await setLocation(12) //地区题函数，只需要传 题号(12) 参数即可；同时在函数前加一个await和空格
 
    //到此结束，下面的代码可以不用管了；你需要关注的代码就是：
    //①问卷链接需要替换
    //②刷题逻辑
    //③不要删除此行下面的任何代码求求了；只能改你的问卷链接和刷题逻辑的代码，其余不要删；
    //④改完代码记得保存！ctrl+s的那种保存！
    //建议使用chrome浏览器，edge可能会出现一些不可预料的“特性”
    //提交的时候如果出现验证报错，你需要更换设备ip，或者手动提交（2023-05-27）
    //作者还在GitHub上发布了python版本的代码喔：https://space.bilibili.com/29109990/channel/collectiondetail?sid=1340503&ctype=0；
    //https://github.com/Zemelee/wjx/blob/master/wjx2.py，如果可以请同学们在github上给个免费的star哇!!!
    //功能比此js版强大一些，可以跳过智能验证，也可以切换ip，代码链接在视频简介里
 
    getCount();
    reset();
    submit();
    window.scrollTo(0, document.body.scrollHeight)
 
    function setCount() {
        localforage.getItem('wjx_count').then(e => {
            let wjx_count = e || 0; // 如果e为null则设为0
            wjx_count++;
            // 将其存回 localForage
            localforage.setItem('wjx_count', wjx_count)
        })
    }
    function getCount() {
        localforage.getItem('wjx_count').then(e => {
            let wjx_count = e || 0; // 如果e为null则设为0
            // 将其存回 localForage
            localforage.setItem('wjx_count', wjx_count)
                .then(() => {
                    // 创建元素
                    createButton(wjx_count)
                })
        }).catch()
    }
 
    // 创建显示数量的元素
    function createButton(count) {
        var parentElement = document.getElementById("ctlNext");
        var divAlert = document.createElement("div");
        divAlert.innerHTML = `已填写${count}份`;
        divAlert.style.backgroundColor = "blue";
        divAlert.style.color = "white";
        divAlert.style.border = "none";
        divAlert.style.textAlign = "center";
        divAlert.style.padding = "10px 20px";
        divAlert.style.margin = "10px";
        parentElement.appendChild(divAlert);
    }
    // 清0按钮
    function reset() {
        var parentElement = document.getElementById("ctlNext");
        var resetButton = document.createElement("button");
        resetButton.innerHTML = "点我可以把份数清0,重新计数哦!";
        resetButton.style.backgroundColor = "red";
        resetButton.style.color = "white";
        resetButton.style.cursor = "pointer";
        resetButton.style.textAlign = "center";
        resetButton.style.padding = "10px 20px";
        resetButton.style.margin = "10px";
        // 清0
        resetButton.addEventListener("click", function (e) {
            e.stopPropagation;
            // 设置 localForage 中的 wjx_count 为 0
            localforage.setItem('wjx_count', 0).then(e => {
                console.log("wjx_count 已重置为 0");
            }).catch(function (error) {
                console.error("重置 wjx_count 时出错:", error);
            });
        });
        parentElement.appendChild(resetButton);
    }
 
    async function submit() {
        let refreshCount = 0;
        QDPOYIt1();
        // 延迟 1 秒后点击确认按钮
        await new Promise((resolve) => {
            setTimeout(() => {
                //点击提交按钮
                const nextBtn = document.evaluate('//*[@id="ctlNext"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (nextBtn) {
                    nextBtn.click();
                    resolve();
                }
            }, 5000);
        });
 
        // 延迟 2 秒后点击验证按钮
        await new Promise((resolve) => {
            setTimeout(() => {
                document.querySelector('#rectMask').click();
                resolve();
            }, 2000);
        });
        while (refreshCount <= 2) {
            // 延迟 4 秒后执行 simulateSliderVerification 函数
            await new Promise((resolve) => {
                setTimeout(() => {
                    simulateSliderVerification();
                    QDPOYIt1();
                    resolve();
                }, 4000);
            });
 
            await new Promise((resolve, rej) => {
                setTimeout(() => {
                    refresh();
 
                }, 4000)
                resolve()
            })
            clearAll();
            refreshCount += 1
        }
        location.reload();
    }
    //滑动验证函数
    async function simulateSliderVerification() {
        const slider = document.querySelector('#nc_1__scale_text > span');
        console.log("slider", slider)
        if (slider.textContent.startsWith('请按住滑块')) {
            const width = slider.offsetWidth;
            const eventOptions = { bubbles: true, cancelable: true };
            const dragStartEvent = new MouseEvent('mousedown', eventOptions);
            const dragEndEvent = new MouseEvent('mouseup', eventOptions);
            const steps = 10;
            const stepWidth = width / steps;
            let currX = stepWidth / 2;
            slider.dispatchEvent(dragStartEvent);
            const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
            for (let i = 0; i < steps; i++) {
                const randomTime = Math.random() * 100 + 50
                slider.dispatchEvent(new MouseEvent('mousemove', Object.assign({ clientX: currX }, eventOptions)));
                currX += stepWidth;
                await delay(randomTime);
            }
            slider.dispatchEvent(dragEndEvent);
            console.log("滑动完成")
        }
    }
    async function refresh() {
        document.querySelector("#nc_1_refresh1").click()
    }
    //下一页
    function nextPage() {
        document.querySelector('a.button.mainBgColor').click();
    }
 
    //单选题函数
    function single(current, ratio) {
        try {
            current = current - 1
            var lists = document.querySelectorAll('.field.ui-field-contain')
            //该单选题的选项
            var ops = lists[current].getElementsByClassName('ui-controlgroup')[0].children
            ratio = normArray(ratio)
            var index = singleRatio([1, ops.length], ratio)
            ops[index - 1].click()
            console.log("第", current + 1, "题选择了第", index, "个选项")
            return index
        } catch {
            console.log("第", current + 1, "题错误")
        }
 
    }
    //多选题函数
    function multiple(current, ratio) {
        try {
            current = current - 1
            var lists = document.querySelectorAll('.field.ui-field-contain')
            //该多选题的选项
            var ops = lists[current].getElementsByClassName('ui-controlgroup')[0].children
            let mul_list = [];
            // 获取随机数列表
            function getRandomNumberList(ratio, mul_list) {
                return ratio.map((item) => Math.random() < item / 100 ? 1 : 0);
            }
            while (mul_list.reduce((acc, curr) => acc + curr, 0) <= 0) {
                mul_list = getRandomNumberList(ratio, mul_list);
            }
            for (const [index, item] of mul_list.entries()) {
                if (item == 1) {
                    ops[index].click()
                    console.log("第", current + 1, "题选择了第", index + 1, "个选项")
                }
            }
        } catch { }
 
    }
    //矩阵题函数
    function matrix(current, matrix_prob) {
        try {
            const xpath1 = `//*[@id="divRefTab${current}"]/tbody/tr`;
            const a = document.evaluate(xpath1, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
            let q_num = 0;
            //遍历每项判断是否为题
            for (let i = 0; i < a.snapshotLength; i++) {
                const tr = a.snapshotItem(i);
                if (tr.getAttribute("rowindex") !== null) {
                    q_num++;
                }
            }
            const xpath2 = `//*[@id="drv${current}_1"]/td`;
            const b = document.evaluate(xpath2, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
            // 矩阵题的选项数量
            const optionCount = b.snapshotLength - 1;
            // 转嵌套的数组
            const matrix_arrays = Object.values(matrix_prob);
            // 遍历每个数组并归一化
            const normalizedArrays = matrix_arrays.map((arr) => {
                return normArray(arr)
            });
            for (let i = 1; i <= q_num; i++) {
                //生成[2,optionCount]之间的随机数
                var opt = singleRatio([2, optionCount + 1], normalizedArrays[i - 1])
                var nthElement = document.querySelectorAll(`#drv${current}_${i} td`)[opt - 1];
                nthElement.click()
            }
        } catch { }
    }
 
    function scale(current, ratio) {
        try {
            let xpath = `//*[@id="div${current}"]/div[2]/div/ul/li`;
            let a = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
            let b = singleRatio([1, a.snapshotLength], ratio);
            let element = document.querySelector(`#div${current} > div.scale-div > div > ul > li:nth-child(${b})`);
            element.click();
            console.log("第", current, "题选择了第", b, "个选项")
            return b
        } catch { }
 
    }
 
    function slide(current, min, max) {
        try {
            var score = randint(min, max)
            document.querySelector(`#q${current}`).value = score
            console.log("第", current, "题填写了", score)
        } catch { }
    }
    //填空题函数
    function vacant(current, texts, ratio) {
        try {
            var text_index = singleRatio([0, texts.length - 1], ratio)
            document.querySelector(`#q${current}`).value = texts[text_index]
            console.log("第", current, "题填写了", texts[text_index])
        } catch { }
 
    }
    async function setLocation(current) {
        document.querySelector(`#q${current}`).click()
        // await new Promise((resolve) => { setTimeout(resolve, 3000); });
        await new Promise((resolve) => {
            const observer = new MutationObserver(() => {
                if (document.querySelector("#divFrameData>script")) {
                    observer.disconnect();
                    resolve();
                }
            });
            observer.observe(document.body, { childList: true, subtree: true });
            if (document.querySelector("#divFrameData>script")) {
                observer.disconnect();
                resolve();
            }
        });
        //----------------------------province
        document.querySelector("#divFrameData>div>div.ui-select.divProvince>div>span>span.selection>span")
            .dispatchEvent(new MouseEvent('mousedown'));//点击省份按钮
        await new Promise((resolve) => { setTimeout(resolve, 500); });
        let provinceList = document.querySelectorAll("[id^=select2-province][id$=-results]>li");
        let pIndex = randint(1, provinceList.length - 1)
        provinceList[pIndex].dispatchEvent(new MouseEvent('mouseup', {
            bubbles: true,
        })); //选择省份
        await new Promise((resolve) => { setTimeout(resolve, 500); });
        //----------------------------city
        document.querySelector("#divFrameData>div>div:nth-child(3)>div>span>span.selection>span")
            .dispatchEvent(new MouseEvent('mousedown')); //点击城市按钮
        await new Promise((resolve) => { setTimeout(resolve, 500); });
        let cityList = document.querySelectorAll("[id^=select2-city][id$=-results]>li");
        let cIndex = randint(1, cityList.length-1)
        console.log(cityList,cIndex)
        await new Promise((resolve) => { setTimeout(resolve, 500); });
        cityList[cIndex].dispatchEvent(new MouseEvent('mouseup', {
            bubbles: true,
        })); //选择城市
        await new Promise((resolve) => { setTimeout(resolve, 700); });
        //----------------------------area(optional)
        try {
            document.querySelector("#divFrameData>div>div:nth-child(4)>div>span>span.selection>span")
                .dispatchEvent(new MouseEvent('mousedown'));//点击地区按钮
            await new Promise((resolve) => { setTimeout(resolve, 1000); });
            let areaList = document.querySelectorAll("[id^=select2-area][id$=-results]>li");
            let aIndex = randint(1, areaList.length-1)
            areaList[aIndex].dispatchEvent(new MouseEvent('mouseup', {
                bubbles: true,
            })); //选择地区
            await new Promise((resolve) => { setTimeout(resolve, 500); });
        } catch { }
        document.querySelector("#divFrameData>div div.save_btn.layer_save_btn > a").click()
 
    }
 
    async function reorder(current) {
        let orderList = document.querySelectorAll(`#div${current}>ul>li`);
        for (let i = 0; i < orderList.length; i++) {
            orderList = document.querySelectorAll(`#div${current}>ul>li`)
            orderList[randint(i, orderList.length - 1)].click()
            await new Promise((resolve) => { setTimeout(resolve, 1000) })
        }
    }
 
    function normArray(arr) {
        const sum = arr.reduce((accum, val) => accum + val, 0);
        return arr.map(val => val / sum);
    }
 
    function singleRatio(range, ratio) {
        let weight = [];
        let sum = 0;
        for (let i = range[0]; i <= range[1]; i++) {
            sum += ratio[i - range[0]];
            weight.push(sum);
        }
        const rand = Math.random() * sum;
        for (let i = 0; i < weight.length; i++) {
            if (rand < weight[i]) {
                return i + range[0];
            }
        }
    }
 
    function randint(a, b) {
        return Math.floor(Math.random() * (b - a + 1) + a);
    }
 
    // 允许右键和复制
    document.oncontextmenu = function () {
        return true;
    };
    document.onselectstart = function () {
        return true;
    };
    function clearAll() {
        var cookies = document.cookie.split("; ");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i];
            var eqPos = cookie.indexOf("=");
            var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
            document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
        }
        sessionStorage.clear();
        localStorage.clear();
    }
    $("body").css("user-select", "text");
    function QDPOYIt1() { for (let i = 0; i < randint(14, 130); i++) { $("\x23\x64\x69\x76\x31")['\x74\x72\x69\x67\x67\x65\x72']("\x6d\x6f\x75\x73\x65\x6f\x76\x65\x72") } }
    function showMessage(text) {
        let messageBox = document.createElement('div');
        messageBox.textContent = text;
        messageBox.style.cssText = `
        position: fixed;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        z-index: 9999;
    `;
        document.body.appendChild(messageBox);
        setTimeout(() => {
            messageBox.style.display = 'none';
        }, 4000);
    }
})();
