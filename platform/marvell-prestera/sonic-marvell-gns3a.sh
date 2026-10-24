#!/bin/bash

# This script creates a .gns3a SONiC appliance file for the marvell-prestera-psai-vs KVM image.
IMGFILE="sonic-marvell-prestera-psai-vs.img"
RELEASE="latest"

usage() {
    echo "`basename $0` [ -r <ReleaseNumber> ] -b <SONiC VS image: sonic-marvell-prestera-psai-vs.img>"
    echo "e.g.: `basename $0` -r 1.1 -b <store_path>/sonic-marvell-prestera-psai-vs.img"
    exit 0
}

while getopts "r:b:h" arg; do
  case $arg in
    h)
	usage
	;;
    r)
	RELEASE=$OPTARG
	;;
    b)
	IMGFILE=$OPTARG
	;;
  esac
done

if [ ! -e ${IMGFILE} ]; then
    echo "ERROR: ${IMGFILE} not found"
    exit 2
fi


MD5SUMIMGFILE=`md5sum  ${IMGFILE} | cut -f 1 -d " "`
LENIMGFILE=`stat -c %s ${IMGFILE}`
GNS3APPNAME="SONiC-marvell-prestera-psai-vs-${RELEASE}.gns3a"
NAMEIMGFILE=`basename $IMGFILE`

echo "
{
    \"name\": \"SONiC-marvell-prestera-psai-vs\",
    \"category\": \"router\",
    \"description\": \"SONiC Marvell Prestera Virtual Switch/Router\",
    \"vendor_name\": \"Marvell\",
    \"vendor_url\": \"https://sonic-net.github.io/SONiC/\",
    \"product_name\": \"SONiC-marvell-prestera-psai-vs\",
    \"product_url\": \"https://sonic-net.github.io/SONiC/\",
    \"registry_version\": 3,
    \"status\": \"experimental\",
    \"maintainer\": \"Marvell\",
    \"maintainer_email\": \"test@marvell.com\",
    \"usage\": \"Supports SONiC release: ${RELEASE}\",
    \"first_port_name\": \"eth0\",
    \"qemu\": {
        \"adapter_type\": \"e1000\",
        \"adapters\": 36,
        \"ram\": 4096,
        \"cpus\": 2,
        \"hda_disk_interface\": \"virtio\",
        \"arch\": \"x86_64\",
        \"console_type\": \"telnet\",
        \"boot_priority\": \"d\",
        \"kvm\": \"require\"
    },
    \"images\": [
        {
            \"filename\": \"${NAMEIMGFILE}\",
            \"version\": \"${RELEASE}\",
            \"md5sum\": \"${MD5SUMIMGFILE}\",
            \"filesize\": ${LENIMGFILE}
        }
    ],
    \"versions\": [
        {
            \"name\": \"${RELEASE}\",
            \"images\": {
                \"hda_disk_image\": \"${NAMEIMGFILE}\"
            }
        }
    ]
}

" > ${GNS3APPNAME}
