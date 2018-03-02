const puppeteer = require('puppeteer');
const http = require('http');
const urllib = require('url');
const now = require('dateformat');

const server = http.createServer((req, res) => {
    console.log(now(), 'request: ' + req.url);
	res.writeHead(200, {'Content-Type':'application/json'});

	const parse = urllib.parse(req.url, true);
	const query = parse.query;
	
	if (query['url'] != undefined) {
		download(query['url'], res);
	}
	else {
		err = 'missing parameter "url"';
		res.write(JSON.stringify({err:err}));
		res.end();
	}
});

const download = ((url, res) => {
	(async () => {
		const browser = await puppeteer.launch();
		const page = await browser.newPage();
	
		try {
			await page.goto(url);
			await page.waitForFunction('document.querySelectorAll("#Main tr").length > 2', {timeout:10000});
            await page.waitFor(1000);
		}
		catch (e) {
			console.error(now(), e.message);
		}

		const html = await page.evaluate('document.documentElement.outerHTML');

		//page.close();
		browser.close();

		res.write(JSON.stringify({ok:0,url:url,createAt:now('isoDateTime'),html:html}));
		res.end();
	})();
});

server.listen(8888);
console.log(now(), 'Node.js runing on port 8888');
