from FlaskManager import Controller, ControllerMethod
from OpenApiKey import Key as k
from OpenApiKey import HiddenKey as hk
import OpenApiBasic as basic
import OpenApiManager as docApi
import HttpStatus


@Controller(url='/swagger-io')
class DocumentationController:

    @ControllerMethod(url='/')
    def get(self):
        swaggerDocumentation = docApi.swaggerDocumentation(**{
            **docApi.info(**{
                k.TITLE : 'My first api',
                k.VERSION : '0.0.1'
            }),
            **docApi.tags(
                docApi.tag(**{
                    k.NAME : 'My tag'
                })
            ),
            **docApi.paths({
                **docApi.path(**{
                    hk.PATH : '/my/path',
                    **docApi.verbDict(
                        **docApi.verb(**{
                            hk.VERB : 'post',
                            **docApi.tags('My tag'),
                            k.DESCRIPTION : "it's my post path",
                            k.OPERATION_ID : 'key'
                        })
                    ),
                    **docApi.verbDict(
                        **docApi.verb(**{
                            hk.VERB : 'get',
                            **docApi.tags('My tag'),
                            k.DESCRIPTION : "it's my get path",
                            k.OPERATION_ID : 'key'
                        })
                    )
                })
            }),
            **docApi.definitions({
                **docApi.definition(**{
                    hk.DEFINITION : 'SomeObjectDefinition',
                    k.TYPE : 'object',
                    **docApi.required('username','password'),
                    **docApi.properties({
                        **docApi.property(**{
                            hk.PROPERTY : 'username',
                            k.TYPE : 'string'
                        }),
                        **docApi.property(**{
                            hk.PROPERTY : 'password',
                            k.TYPE : 'string',
                            k.EXAMPLE : '123asd*&(QWE'
                        })
                    })
                }),
                **docApi.definition(**{
                    hk.DEFINITION : 'AnotherObjectDefinition',
                    k.TYPE : 'object'
                })
            })
        })
        # print(swaggerDocumentation)
        # import json
        # print(json.dumps(swaggerDocumentation))
        return swaggerDocumentation, HttpStatus.OK
