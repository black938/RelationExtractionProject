var url = 'http://127.0.0.1:4236/api/extractTriples?sentence='

var app_para = new Vue({
    el: '#para',
    data: {
        para: '天龙八部《天龙八部》是由张纪中担任总制片人，周晓文、于敏等联合执导的古装武侠爱情剧，由胡军、林志颖、高虎、刘亦菲、刘涛、陈好、修庆等联袂主演'
    },
    methods: {
        getAPI: function () {
            var s = url + this.para
            main(s)
        }
    }
})

var app_resp = new Vue({
    el: '#resp',
    data: {
        response: null
    },
})

var app_ner = new Vue({
    el: '#ner',
    data: {
        ners: [

        ]
    }
})

var app_relation = new Vue({
    el: '#relation',
    data: {
        relations: [

        ]
    }
})

var option;
option = {
    title: {
        text: '关系抽取可视化'
    },
    tooltip: {},
    animationDurationUpdate: 1500,
    animationEasingUpdate: 'quinticInOut',
    series: [
        {
            type: 'graph',
            color: ['#009688'],
            layout: 'circular',
            symbolSize: 50,
            roam: false,
            label: {
                show: true
            },
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 10],
            edgeLabel: {
                normal: {
                    fontSize: 15,
                    show: true,
                    formatter: function (x) {
                        return x.data.name;
                    }
                }
            },
            data: [],
            // links: [],
            links: [],
            lineStyle: {
                type: 'dotted',
                opacity: 0.8,
                width: 2.5,
                curveness: 0.2
            },
        }
    ]
};

function main(url) {
    var jqxhr = $.getJSON(url).done(function (data) {
        var resp = ''
        var ner = new Set()
        var relation = new Set()
        option.series[0].data=[]
        option.series[0].links=[]
        // app_resp的赋值
        resp = data
        app_resp.response = resp;
        // app_ner的赋值
        // app_relation的赋值
        app_ner.ners = []
        app_relation.relations = []
        for (var i = 0; i < resp.data.length; i++) {
            ner.add(resp.data[i].obj1)
            ner.add(resp.data[i].obj2)
            relation.add(resp.data[i].relation)
        }
        for (var n of ner) {
            app_ner.ners.push({ ner: n })
        }
        for (var r of relation) {
            app_relation.relations.push({ relation: r })
        }
        // option的赋值
        for (var n of ner) {
            option.series[0].data.push({ name: n })
        }
        for (var i = 0; i < resp.data.length; i++) {
            option.series[0].links.push(
                {
                    source: resp.data[i].obj1,
                    target: resp.data[i].obj2,
                    name: resp.data[i].relation
                })
        }
        draw(option);
    });

}

function draw(option) {
    var chartDom = document.getElementById('main');
    var myChart = echarts.init(chartDom);
    option && myChart.setOption(option);

}
