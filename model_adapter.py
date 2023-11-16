import dtlpy as dl
import logging
import os

logger = logging.getLogger('FailTestAdapter')


@dl.Package.decorators.module(description='Test Model Adapter for failing model',
                              name='model-adapter',
                              init_inputs={'model_entity': dl.Model})
class Adapter(dl.BaseModelAdapter):
    def save(self, local_path, **kwargs):
        raise NotImplementedError('save is not implemented')

    def convert_from_dtlpy(self, data_path, **kwargs):
        raise NotImplementedError('convert_from_dtlpy is not implemented')

    def load(self, local_path, **kwargs):
        raise NotImplementedError('convert_from_dtlpy is not implemented')

    def train(self, data_path, output_path, **kwargs):
        raise NotImplementedError('train is not implemented')

    def prepare_item_func(self, item):
        raise NotImplementedError('prepare_item_func is not implemented')

    def predict(self, batch, **kwargs):
        raise NotImplementedError('predict is not implemented')

    def export(self):
        raise NotImplementedError('export is not implemented')


def package_creation(project: dl.Project):
    metadata = dl.Package.get_ml_metadata(
        cls=Adapter,
        default_configuration={},
        output_type=dl.AnnotationType.BOX,

    )
    modules = dl.PackageModule.from_entry_point(entry_point='model_adapter.py')

    package = project.packages.push(
        package_name='fail-model-init',
        src_path=os.getcwd(),
        is_global=False,
        package_type='ml',
        codebase=dl.GitCodebase(
            git_url='https://github.com/AharonDL/fail-model.git',
            git_tag='failing-model-init'
        ),
        modules=[modules],
        service_config={
            'runtime': dl.KubernetesRuntime(
                pod_type=dl.INSTANCE_CATALOG_REGULAR_XS,
                autoscaler=dl.KubernetesRabbitmqAutoscaler(
                    min_replicas=0,
                    max_replicas=1),
                preemptible=True,
                concurrency=1
            ).to_json(),
            'initParams': {'model_entity': None}
        },
        metadata=metadata
    )
    return package


def model_creation(package: dl.Package):
    model = package.models.create(
        model_name='failing-model-init',
        description='Failing model',
        tags=[],
        dataset_id=None,
        status='trained',
        scope='project',
        configuration={},
        project_id=package.project.id,
        labels=['1', '2'],
        input_type='image',
        output_type='box'
    )
    return model


def deploy():
    dl.setenv('rc')
    project = dl.projects.get(project_id='d59ee7e5-2fe9-4379-90cf-edfcd84f1008')
    package_creation(project=project)


if __name__ == "__main__":
    deploy()
