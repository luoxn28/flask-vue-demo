<template>
  <div>

    <div class="block">
      <el-cascader
        placeholder="处理策略"
        v-model="value"
        :options="options"
        :props="{ expandTrigger: 'hover'}"
        :clearable=true
        @change="handleChange"></el-cascader>
    </div>

    <!--表头选择 默认前1行为表头行-->
    <el-row class="row-head" :gutter="5">
      <el-col :span="6">
        <div class="head-options">
          <el-select v-model="head_value" placeholder="请选择文章标签">
            <el-option v-for="item in head_options" :key="item.value" :label="item.label"
                       :value="item.value"></el-option>
          </el-select>
          <el-tooltip class="item" content="表示表格中前多少行是表头信息" placement="top-start">
            <i class="el-icon-question"></i>
          </el-tooltip>
        </div>
      </el-col>
    </el-row>

    <!--选择框-->
    <el-row :gutter="5">
      <el-col :span="18">
        <el-input v-model="input" placeholder="请输入表达式，比如: v[0]>1 and v[0]<10" style="color: red"></el-input>
      </el-col>
      <el-col :span="2">
        <el-button type="primary" icon="el-icon-search" @click="input_click">搜索</el-button>
      </el-col>
    </el-row>

    <!--查询框-->
    <div class="query-data-div">
      <el-row :gutter="20">
        <el-table :data="query_data">
          <el-table-column>
            <template slot-scope="scope">
              <!--增加/减少输入框-->
              <el-col :span="1">
                <el-button icon="el-icon-minus" type="info" :disabled="query_data[scope.$index].sub"
                           @click="del_query_data(scope.$index)"></el-button>
              </el-col>
              <el-col :span="1" style="margin-right: 2px;">
                <el-button icon="el-icon-plus" type="success"
                           :disabled="query_data.length>1 && scope.$index<query_data.length-1"
                           @click="add_query_data(scope.$index)"></el-button>
              </el-col>

              <!--输入框-->
              <el-col :span="14">
                <el-input v-model="query_data[scope.$index].input"
                          :placeholder="query_input_placeholder[query_data[scope.$index].input_type]"></el-input>
              </el-col>

              <el-col :span="5">
                <div class="head-options">
                  <el-select v-model="query_data[scope.$index].input_type" placeholder="表达式">
                    <el-option v-for="item in query_input_options" :key="item.value" :label="item.label"
                               :value="item.value"></el-option>
                  </el-select>
                  <el-tooltip class="item" content="注意输入的符号都必须是英文符号，比如英文逗号','或者英文括号'()'" placement="top">
                    <i class="el-icon-question"></i>
                  </el-tooltip>
                </div>
              </el-col>

              <el-col :span="2" v-if="scope.$index===query_data.length-1">
                <el-button type="primary" icon="el-icon-search" @click="input_click_query_data">搜索</el-button>
              </el-col>
            </template>
          </el-table-column>
        </el-table>
      </el-row>
    </div>

    <!--https://element.eleme.cn/#/zh-CN/component/table-->
    <el-table class="table-excel" v-if="dataList.length!==0" :data="dataList" :span-method="excelSpanMethod" border
              style="width: 100%">
      <!-- 动态生成列 -->
      <el-table-column v-for="(item, index) in headerList" :prop="item" :label="item">
        <template slot-scope="scope">
          <div>{{ scope.row[item][0].toString() }}</div>
        </template>
      </el-table-column>
    </el-table>

  </div>
</template>

<script>
  export default {
    name: "Excel",
    data() {
      return {
        excel_filepath: '',
        excel_sheet: '',

        // 表头信息
        head_options: [
          {value: 1, label: '第1行 (表头信息)'},
          {value: 2, label: '前2行 (表头信息)'},
          {value: 3, label: '前3行 (表头信息)'}],
        head_value: 1,

        // 查询条件信息
        query_data: [{'sub': true, 'input_type': 0}],
        query_input_placeholder: [
          '请输入表达式，比如: (v[0]>1 and v[0]<10)',
          '请输入排序字段，如果排序字段超过1个请以英文逗号分隔，比如: v[1] 或者 v[1], v[2]'
        ],
        query_input_options: [
          {value: 0, label: '表达式'},
          {value: 1, label: '排序 (正序)'},
          {value: 2, label: '排序 (倒序)'}
        ],

        value: [],
        options: [
          {
            value: 'ziyuan',
            label: '资源'
          },
          {
            value: 'color',
            label: '着色',
            children: [
              {
                value: 'font',
                label: '文本',
                children: [
                  {
                    value: 'blue',
                    label: '蓝色',
                  }
                ]
              },
              {
                value: 'background',
                label: '背景',
                children: [
                  {
                    value: 'red',
                    label: '红色',
                  }
                ]
              }
            ]
          }
        ],
        input: '',
        input_enable: false,

        headerList: [],
        dataList: []
      }
    },

    methods: {
      add_query_data(index) {
        this.query_data.push({'input_type': 0});
      },
      del_query_data(index) {
        this.query_data.splice(index, 1);
      },
      input_click_query_data() {
        for (let i = 0; i < this.query_data.length; i++) {
          let value = this.query_data[i]
          if (!value.hasOwnProperty('input') || value['input'] === null || value['input'] === '') {
            this.$message.error(this.query_data.length === 1 ? '查询条件为空' : '有些查询条件为空')
            return
          }
        }

        console.log(this.query_data)
        this.axios.post("/api/hello/sheet/data", {
          "path": this.excel_filepath,
          "sheet": this.excel_sheet,
          'query_data': this.query_data,
          'head_value': this.head_value
        }).then(res => {
          if ((res = res['data'])['code'] !== 0) {
            this.$message.error(res['msg'])
            return
          }

          console.log(res)

          // 提取表头列表&数据
          let headerList = [], dataList = []
          for (const v of res['data'][0]) {
            headerList.push(v[0])
          }
          for (let i = 1; i < res['data'].length; i++) {
            let data = {}
            for (let j = 0; j < res['data'][i].length; j++) {
              data[headerList[j]] = res['data'][i][j]
            }
            dataList.push(data)
          }

          this.dataList = dataList;
          this.headerList = headerList;
          this.input_enable = true
        }).catch(res => {
          this.$message.error(res)
        })
      },

      init() {
        this.axios.post("/api/current/sheet/name", {}).then(res => {
          if ((res = res['data'])['code'] !== 0) {
            this.$message.error(res['msg'])
            return
          } else if ((res = res['data']).length !== 2 || res[0].length === 0 || res[1].length === 0) {
            console.log('还未加载文件', res)
            return;
          }

          console.log('已加载文件', res)
          this.listSheetData(res[0], res[1], '')
        })
      },

      handleChange(value) {
        if (value.length === 0) {
          return
        }

        console.log(value);
      },

      input_click() {
        console.info(this.input)
        this.listSheetData(this.excel_filepath, this.excel_sheet, this.input)
      },

      excelSpanMethod({row, column, rowIndex, columnIndex}) {
        if (rowIndex >= this.dataList.length || columnIndex >= this.dataList[rowIndex].length) {
          return [1, 1]
        }

        let data = this.dataList[rowIndex][this.headerList[columnIndex]]
        if (data[1] === 1) {
          return [data[2], data[3]]
        } else if (data[1] === -1) {
          return [0, 0]
        }

        return [1, 1]
      },

      // 获取excel文件sheet名称列表
      listSheetNames(path) {
        this.axios.post("/api/query/sheet/names", {
          "path": path
        }).then(res => {
          res = res['data']
          if (res['code'] !== 0) {
            this.$message.error(res['msg'])
            return
          }

          // 默认展示第一个sheet内容
          this.listSheetData(path, res['data'][0], '')
        }).catch(res => {
          this.$message.error(res['data']['msg'])
        })
      },

      // 获取excel某个sheet内容
      listSheetData(path, sheet, lambda) {
        this.axios.post("/api/query/sheet/data", {
          "path": path, "sheet": sheet, 'lambda': lambda, 'head_value': this.head_value
        }).then(res => {
          res = res['data']
          if (res['code'] !== 0) {
            this.$message.error(res['msg'])
            return
          }

          this.excel_filepath = path
          this.excel_sheet = sheet

          // 提取表头列表&数据
          let headerList = [], dataList = []
          for (const v of res['data'][0]) {
            headerList.push(v[0])
          }
          for (let i = 1; i < res['data'].length; i++) {
            let data = {}
            for (let j = 0; j < res['data'][i].length; j++) {
              data[headerList[j]] = res['data'][i][j]
            }
            dataList.push(data)
          }

          this.dataList = dataList;
          this.headerList = headerList;
          this.input_enable = true
        }).catch(res => {
          this.$message.error(res)
        })
      }
    },

    mounted() {
      this.init()
    }
  }
</script>

<style scoped>
  .row-head {
    margin-top: 10px;
    margin-bottom: 10px;
  }

  .head-options {
    color: #409EFF;
  }

  .query-data-div {

  }

  .table-excel {
    /*color: #409EFF;*/
    margin-top: 10px;
  }
</style>
