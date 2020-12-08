(function () {
  function baixarDados() {
    var params = {
      municipio: { id: 1600709 },
      email: "test@test.com",
      captcha: "u6bsa",
    };

    var tipoDownload = "shapefile";

    var url = "../municipios/" + tipoDownload + "?" + $.param(params);

    var hiddenIFrameId = "hiddenDownloader";

    var iframe = document.getElementById(hiddenIFrameId);

    if (iframe === null) {
      iframe = document.createElement("iframe");
      iframe.id = hiddenIFrameId;
      iframe.style.display = "none";
      iframe.onload = function () {
        var dados = {
          status: "sucesso",
          mensagem: "Arquivo gerado com sucesso",
        };
      };
      document.body.appendChild(iframe);
    }

    iframe.src = url;

    var iframes = document.querySelectorAll("iframe");
    for (var i = 0; i < iframes.length; i++) {
      iframes[i].parentNode.removeChild(iframes[i]);
    }
  }
})();
