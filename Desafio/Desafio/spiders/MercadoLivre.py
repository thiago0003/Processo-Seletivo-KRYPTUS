import scrapy

class AuthorSpider(scrapy.Spider):
    contador = 1

    #Dados do projeto
    name = 'mercadoLivre'
    start_urls = ['https://lista.mercadolivre.com.br/tenis-nike#D[A:tenis%20nike]/']

    def parse(self, response):

        #Percorre os item da página
        for itens in response.css('.ui-search-layout__item'):

            #Validação do valor em centavos do item
            centavos = itens.css('.ui-search-price__second-line .price-tag-cents::text').get()
            if centavos == None:
                centavos = '00' 

            #Validação do valor em centavos do item parcelado
            centavos_parcelado = itens.css('.ui-search-color--LIGHT_GREEN .ui-search-price__part .price-tag-cents::text').get()
            if centavos_parcelado == None:
                centavos_parcelado = '00'

            #Validação no preço parcelado caso a classe seja diferente do padrão
            valor_parcelado = itens.css('.ui-search-color--LIGHT_GREEN .ui-search-price__part .price-tag-fraction::text').get()
            if valor_parcelado == None:
                valor_parcelado = itens.css('.ui-search-color--BLACK .ui-search-price__part .price-tag-fraction::text').get()
            
            #Monta os dados
            yield {
                'Preço': itens.css('.ui-search-price__second-line .price-tag-fraction::text').get() + ',' + centavos,
                'Preco parcelado' : itens.css('.ui-search-installments::text').get() + valor_parcelado  + ',' + centavos_parcelado,
                'Nome' : itens.css('.ui-search-item__title::text').get(),
                'Foto' : itens.css('.slick-slide img::attr(data-src)').get(),
                'Tipo de frete' : itens.css('.ui-search-item__shipping--free::text').get(),
                'Nome loja' : itens.css('.ui-search-official-store-label::text').get(),
                'Link' : itens.css('a.ui-search-result__content::attr(href)').get(),
                'id produto' : itens.css('.ui-search-result__bookmark [name="itemId"]::attr(value)').get(),
                'item patrocinado' : itens.css('.ui-search-item__ad-label--blue::text').get(),
            }

        #Verifica a quantidade de vezes
        if self.contador < 5:

            #Inclementa o contador
            self.contador += 1
        
            #Recebe o link para a próxima página
            pagination_links = response.css('.andes-pagination__button--next a.andes-pagination__link::attr(href)').get() 
            yield scrapy.Request(response.urljoin(pagination_links))
