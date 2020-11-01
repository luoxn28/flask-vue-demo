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

    <el-input v-model="input" placeholder="请输入表达式"></el-input>
    <el-button v-if="input_enable" type="primary" icon="el-icon-search" @click="input_click">搜索</el-button>

    <!--https://element.eleme.cn/#/zh-CN/component/table-->
    <el-table v-if="dataList.length!==0" :data="dataList" :span-method="excelSpanMethod" border style="width: 100%">
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
        // this.axios.post("/api/hello/sheet/data", {
        this.axios.post("/api/query/sheet/data", {
          "path": path, "sheet": sheet, 'lambda': lambda
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

</style>
