import requests
import json
from urllib.parse import urljoin
from .exceptions import JSONDecodeError, RequestError, ResponseError
from .stacks import Stack
from .services import Service


class Environment(object):
    def __init__(self, url, access_key, secret_key, project_id=None, port=80, api_version='v2-beta'):
        endpoint = urljoin(url + ':' + str(port), api_version + '/projects/' + project_id + '/')
        self.endpoint = endpoint
        self.auth = (access_key, secret_key)
        self.__dict__ = self.request(endpoint[:-1], 'GET')
        self.endpoint = endpoint
        self.auth = (access_key, secret_key)

    def __call__(self):
        print(json.dumps(self.__dict__, indent=4))

    def __str__(self):
        return b'<{:s} at {:#x}>'.format(type(self).__name__, id(self))

    def __unicode__(self):
        return '<{:s} at {:#x}>'.format(type(self).__name__, id(self))

    def __set_content_type(self, headers, ctype):
        headers.update({'content-type': ctype})

    def __get(self, url, params, data, headers):
        return requests.get(url, auth=self.auth, params=params, headers=headers)

    def __post(self, url, params, data, headers):
        self.__set_content_type(headers, 'application/json')
        return requests.post(url, auth=self.auth, data=json.dumps(data), params=params, headers=headers)

    def __put(self, url, params, data, headers):
        self.__set_content_type(headers, 'application/json')
        return requests.put(url, auth=self.auth, data=json.dumps(data), params=params, headers=headers)

    def __delete(self, url, params, data, headers):
        self.__set_content_type(headers, 'application/x-www-form-urlencoded')
        return requests.delete(url, auth=self.auth, params=params, headers=headers)

    def __request(self, url, method, params, data, headers=None):
        headers = headers or {}

        METHODS = {
            'get': self.__get,
            'post': self.__post,
            'put': self.__put,
            'delete': self.__delete
        }

        request_method = METHODS[method.lower()]
        url = urljoin(self.endpoint, url)

        return request_method(url, params=params, data=data, headers=headers)

    def request(self, url, method, params=None, data=None):
        params = params or {}
        data = data or {}

        response = self.__request(url, method, params, data)

        if response.status_code == 204:
            json_response = ''
        else:
            try:
                json_response = response.json()
            except ValueError:
                raise JSONDecodeError()

            if not response.ok:
                if response.status_code >= 500:
                    raise ResponseError(
                        'Server did not respond. {} {}'.format(
                            response.status_code, response.reason))

                raise RequestError('{} {}. Message: {} - {}'.format(
                    response.status_code, response.reason, json_response['code'], json_response['message']))

        return json_response

    # ## ### Actions

    def activate(self):
        return self.request(self.endpoint[:-1], 'POST', params={'action': 'activate'})

    def deactivate(self):
        return self.request(self.endpoint[:-1], 'POST', params={'action': 'deactivate'})

    def upgrade(self):
        return self.request(self.endpoint[:-1], 'POST', params={'action': 'upgrade'})

    def set_members(self):
        # TODO
        pass

    # ## ### API Resources

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/account/
    def account(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/apiKey/
    def api_key(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/auditLog/
    def audit_log(self):
        # TODO check if it's relevant to env
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/certificate/
    def certificate(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/container/
    def container(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/dnsService/
    def dns_service(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/externalService/
    def external_service(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/genericObject/
    def generic_object(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/host/
    def host(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/identity/
    def identity(self):
        # TODO check if it's relevant to env
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/loadBalancerService/
    def load_balancer_service(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/machine/
    def machine(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/machineDriver/
    def machine_driver(self):
        # TODO check if it's relevant to env
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/network/
    def network(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/networkDriver/
    def network_driver(self):
        # TODO check if it's relevant to env
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/networkDriverService/
    def network_driver_service(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/projectMember/
    def project_member(self):
        # TODO check how to implement
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/projectTemplate/
    def project_template(self):
        # TODO check if it's relevant to env
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/pullTask/
    def pull_task(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/registrationToken/
    def registration_token(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/registry/
    def registry(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/registryCredential/
    def registry_credential(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/service/
    def service(self, service_id=None, service_name=None):
        return Service(environment=self, service_id=service_id, service_name=service_name)

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/setting/
    def setting(self):
        # TODO check if it's relevant to env
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/stack/
    def stack(self, stack_id=None, stack_name=None):
        return Stack(environment=self, stack_id=stack_id, stack_name=stack_name)

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/storageDriver/
    def storage_driver(self):
        # TODO check if it's relevant to env
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/storageDriverService/
    def storage_driver_service(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/subnet/
    def subnet(self):
        # TODO check if it's relevant to env
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/subscribe/
    def subscribe(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/volume/
    def volume(self):
        # TODO
        pass

    # http://docs.rancher.com/rancher/v1.3/en/api/v2-beta/api-resources/volumeTemplate/
    def volume_template(self):
        # TODO
        pass
