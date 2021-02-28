'use strict';

import { handler } from '../../src/index';

describe('Tests index', function () {
    it('verifies successful response', async () => {
        const result = await handler(null, null)
        let response = JSON.parse(result.body);
        console.log(response.uuid);
        console.log(response.short_uuid);
        console.log(response.decoded);
    });
});
