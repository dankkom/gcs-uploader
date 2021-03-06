"""Upload datasets to Google Cloud Storage"""


__version__ = "0.0.1"


import argparse
import datetime
import pathlib

from google.cloud import storage


def upload_file(bucket, datasource, source_filepath: pathlib.Path):
    dataset = source_filepath.parent.name
    filename = source_filepath.name
    destination_blob_name = f"{datasource}/{dataset}/{filename}"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_filepath)


def get_blobs_in_bucket(storage_client, bucket, prefix):
    return [o.name for o in storage_client.list_blobs(bucket, prefix=prefix)]


def get_parser():
    parser = argparse.ArgumentParser(
        description="Upload files to Google Cloud Storage",
    )
    parser.add_argument(
        "--bucket",
        required=True,
        help="Bucket name",
    )
    parser.add_argument(
        "--datadir",
        required=True,
        type=pathlib.Path, help="Data directory",
    )
    parser.add_argument(
        "--datasource",
        required=True,
        help="Data source",
    )
    parser.add_argument(
        "--dataset",
        required=False,
        help="Dataset",
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    bucket_name = args.bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    datadir = args.datadir
    datasource = args.datasource
    datasource_dir = datadir / datasource
    if args.dataset:
        dataset_dirs = [datasource_dir / args.dataset]
    else:
        dataset_dirs = sorted(datasource_dir.iterdir(), key=lambda x: x.name)

    i = 0
    for dataset_dir in dataset_dirs:
        dataset_name = dataset_dir.name
        blobs_in_bucket = get_blobs_in_bucket(
            storage_client,
            bucket,
            prefix=f"{datasource}/{dataset_name}",
        )
        for file in sorted(dataset_dir.iterdir(), key=lambda x: x.name):
            filename = file.name
            destination_blob_name = f"{datasource}/{dataset_name}/{filename}"
            if destination_blob_name in blobs_in_bucket:
                print("       Skipping", destination_blob_name)
                continue
            i += 1
            now = f"{datetime.datetime.utcnow():%Y-%m-%d %H:%M:%S.%f}"
            msg = f"{i: >6} {now} {file.name} --> {destination_blob_name}"
            print(msg)
            upload_file(bucket, datasource, file)


if __name__ == "__main__":
    main()
