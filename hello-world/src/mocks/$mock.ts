/* eslint-disable */
import { AxiosInstance } from 'axios'
import mockServer from 'axios-mock-server'
import mock0 from './v1/items/_itemId'
import mock1 from './v1/items'
import mock2 from './v1/groups/_groupId'
import mock3 from './v1/groups'

export default (client?: AxiosInstance) => mockServer([
  {
    path: '/v1/items/_itemId',
    methods: mock0
  },
  {
    path: '/v1/items',
    methods: mock1
  },
  {
    path: '/v1/groups/_groupId',
    methods: mock2
  },
  {
    path: '/v1/groups',
    methods: mock3
  }
], client, '')
