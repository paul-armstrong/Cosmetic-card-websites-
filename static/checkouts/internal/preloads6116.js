
    (function() {
      var baseURL = "https://cdn.shopify.com/shopifycloud/checkout-web/assets/";
      var scripts = ["https://cdn.shopify.com/shopifycloud/checkout-web/assets/runtime.baseline.en.9510b01db0740e45c686.js","https://cdn.shopify.com/shopifycloud/checkout-web/assets/893.baseline.en.4319bef243f469494cc8.js","https://cdn.shopify.com/shopifycloud/checkout-web/assets/961.baseline.en.a5006999a752748861b7.js","https://cdn.shopify.com/shopifycloud/checkout-web/assets/891.baseline.en.a95a4f4f14965c819a76.js","https://cdn.shopify.com/shopifycloud/checkout-web/assets/app.baseline.en.89ac659d20312b80078b.js","https://cdn.shopify.com/shopifycloud/checkout-web/assets/977.baseline.en.ced19ebca9f312cb8c0c.js","https://cdn.shopify.com/shopifycloud/checkout-web/assets/96.baseline.en.a51d92a9365f28b84b4a.js","https://cdn.shopify.com/shopifycloud/checkout-web/assets/307.baseline.en.2db905cbc87f7ff42aa6.js","https://cdn.shopify.com/shopifycloud/checkout-web/assets/OnePage.baseline.en.eb8a72a3d9229e41ca71.js"];
      var styles = ["https://cdn.shopify.com/shopifycloud/checkout-web/assets/893.baseline.en.491cc8e69baeb7620a23.css","https://cdn.shopify.com/shopifycloud/checkout-web/assets/app.baseline.en.9ae7c47c018344a8495b.css","https://cdn.shopify.com/shopifycloud/checkout-web/assets/268.baseline.en.2f7fcc51e79ab3b9a48e.css"];
      var fontPreconnectUrls = ["https://fonts.shopifycdn.com"];
      var fontPrefetchUrls = ["https://fonts.shopifycdn.com/roboto/roboto_n4.da808834c2315f31dd3910e2ae6b1a895d7f73f5.woff2?h1=bG90dXNhcnRzdHVkaW8uY28udWs&hmac=81669bec94fd587e2fec22c9326d3104e879a283e532744fe4dcfc047ceb6bc8","https://fonts.shopifycdn.com/roboto/roboto_n5.126dd24093e910b23578142c0183010eb1f2b9be.woff2?h1=bG90dXNhcnRzdHVkaW8uY28udWs&hmac=59bf8b54119b28bb90ab3e00224ee9839aa3b290a7a99acbbfc111d27f8b745a"];
      var imgPrefetchUrls = ["https://cdn.shopify.com/s/files/1/1484/2792/files/logo-200px_x320.png?v=1613525028"];

      function preconnect(url, callback) {
        var link = document.createElement('link');
        link.rel = 'dns-prefetch preconnect';
        link.href = url;
        link.crossOrigin = '';
        link.onload = link.onerror = callback;
        document.head.appendChild(link);
      }

      function preconnectAssets() {
        var resources = [baseURL].concat(fontPreconnectUrls);
        var index = 0;
        (function next() {
          var res = resources[index++];
          if (res) preconnect(res[0], next);
        })();
      }

      function prefetch(url, as, callback) {
        var link = document.createElement('link');
        if (link.relList.supports('prefetch')) {
          link.rel = 'prefetch';
          link.fetchPriority = 'low';
          link.as = as;
          if (as === 'font') link.type = 'font/woff2';
          link.href = url;
          link.crossOrigin = '';
          link.onload = link.onerror = callback;
          document.head.appendChild(link);
        } else {
          var xhr = new XMLHttpRequest();
          xhr.open('GET', url, true);
          xhr.onloadend = callback;
          xhr.send();
        }
      }

      function prefetchAssets() {
        var resources = [].concat(
          scripts.map(function(url) { return [url, 'script']; }),
          styles.map(function(url) { return [url, 'style']; }),
          fontPrefetchUrls.map(function(url) { return [url, 'font']; }),
          imgPrefetchUrls.map(function(url) { return [url, 'image']; })
        );
        var index = 0;
        (function next() {
          var res = resources[index++];
          if (res) prefetch(res[0], res[1], next);
        })();
      }

      function onLoaded() {
        preconnectAssets();
        prefetchAssets();
      }

      if (document.readyState === 'complete') {
        onLoaded();
      } else {
        addEventListener('load', onLoaded);
      }
    })();
  