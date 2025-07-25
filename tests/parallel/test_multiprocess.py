# Integration tests for plantcv-run-workflow
import os
import pytest
import shutil
from plantcv.parallel import WorkflowConfig
from plantcv.parallel.cli import main


def test_parallel_cli_template(tmpdir):
    """Test for PlantCV."""
    conf_file = tmpdir.mkdir("sub").join("config.json")
    import sys
    sys.argv = ["plantcv-run-workflow", "--template", conf_file.strpath]
    with pytest.raises(SystemExit):
        main()


def test_parallel_cli_invalid_config(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    conf_file = tmpdir.mkdir("cache").join("config.json")
    config = WorkflowConfig()
    config.json = "valid_config.json"
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = parallel_test_data.workflow_script
    config.img_outdir = str(conf_file.dirpath())
    config.save_config(config_file=conf_file.strpath)
    import sys
    sys.argv = ["plantcv-run-workflow", "--config", conf_file.strpath]
    with pytest.raises(ValueError):
        main()


def test_parallel_cli_valid_config(parallel_test_data, tmpdir):
    """Test for PlantCV."""
    conf_file = tmpdir.mkdir("cache").join("config.json")
    config = WorkflowConfig()
    config.input_dir = parallel_test_data.flat_imgdir
    config.json = conf_file.dirpath().join(os.path.basename(parallel_test_data.new_results_file)).strpath
    config.filename_metadata = ["imgtype", "camera", "frame", "zoom", "lifter", "gain", "exposure", "id"]
    config.workflow = parallel_test_data.workflow_script
    config.img_outdir = str(conf_file.dirpath())
    config.tmp_dir = str(conf_file.dirpath() / "tmp")
    config.append = False
    config.save_config(config_file=conf_file.strpath)
    shutil.copy(parallel_test_data.new_results_file, conf_file.dirpath())
    import sys
    sys.argv = ["plantcv-run-workflow", "--config", conf_file.strpath]
    assert main() is None
