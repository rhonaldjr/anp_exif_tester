from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.http import JsonResponse
from fractions import Fraction

import json

from django.contrib.messages.views import SuccessMessageMixin

import datetime

from PIL import Image
import PIL.ExifTags

from imglibrary.models import ImageFile

class ViewImage(SuccessMessageMixin, DetailView):
    template_name = "details.html"
    model = ImageFile

    def _derationalize(self, rational):
        try:
            return rational.numerator / rational.denominator
        except Exception as e:
            print("Exception occured dividing {0}.\n{1}".format(rational, e))
            return 0

    def _create_lookups(self):
        lookups = {}

        lookups["metering_modes"] = ("Undefined",
                                    "Average",
                                    "Center-weighted average",
                                    "Spot",
                                    "Multi-spot",
                                    "Multi-segment",
                                    "Partial")

        lookups["exposure_programs"] = ("Undefined",
                                        "Manual",
                                        "Program AE",
                                        "Aperture-priority AE",
                                        "Shutter speed priority AE",
                                        "Creative (Slow speed)",
                                        "Action (High speed)",
                                        "Portrait ",
                                        "Landscape",
                                        "Bulb")

        lookups["resolution_units"] = ("",
                                    "Undefined",
                                    "Inches",
                                    "Centimetres")

        lookups["orientations"] = ("",
                                "Horizontal",
                                "Mirror horizontal",
                                "Rotate 180",
                                "Mirror vertical",
                                "Mirror horizontal and rotate 270 CW",
                                "Rotate 90 CW",
                                "Mirror horizontal and rotate 90 CW",
                                "Rotate 270 CW")

        return lookups


    def _process_exif_dict(self, exif_dict):

        date_format = "%Y:%m:%d %H:%M:%S"

        lookups = self._create_lookups()

        try:
            exif_dict["DateTime"]["processed"] = \
                datetime.datetime.strptime(exif_dict["DateTime"]["raw"], date_format)

            exif_dict["DateTimeOriginal"]["processed"] = \
                datetime.datetime.strptime(exif_dict["DateTimeOriginal"]["raw"], date_format)

            exif_dict["FNumber"]["processed"] = \
                self._derationalize(exif_dict["FNumber"]["raw"])
            exif_dict["FNumber"]["processed"] = \
                "f{}".format(exif_dict["FNumber"]["processed"])

            exif_dict["MaxApertureValue"]["processed"] = \
                self._derationalize(exif_dict["MaxApertureValue"]["raw"])
            exif_dict["MaxApertureValue"]["processed"] = \
                "f{:2.1f}".format(exif_dict["MaxApertureValue"]["processed"])

            exif_dict["FocalLength"]["processed"] = \
                self._derationalize(exif_dict["FocalLength"]["raw"])
            exif_dict["FocalLength"]["processed"] = \
                "{}mm".format(exif_dict["FocalLength"]["processed"])

            exif_dict["FocalLengthIn35mmFilm"]["processed"] = \
                "{}mm".format(exif_dict["FocalLengthIn35mmFilm"]["raw"])

            exif_dict["Orientation"]["processed"] = \
                lookups["orientations"][exif_dict["Orientation"]["raw"]]

            exif_dict["ResolutionUnit"]["processed"] = \
                lookups["resolution_units"][exif_dict["ResolutionUnit"]["raw"]]

            exif_dict["ExposureProgram"]["processed"] = \
                lookups["exposure_programs"][exif_dict["ExposureProgram"]["raw"]]

            exif_dict["MeteringMode"]["processed"] = \
                lookups["metering_modes"][exif_dict["MeteringMode"]["raw"]]

            exif_dict["XResolution"]["processed"] = \
                int(self._derationalize(exif_dict["XResolution"]["raw"]))

            exif_dict["YResolution"]["processed"] = \
                int(self._derationalize(exif_dict["YResolution"]["raw"]))

            exif_dict["ExposureTime"]["processed"] = \
                self._derationalize(exif_dict["ExposureTime"]["raw"])
            exif_dict["ExposureTime"]["processed"] = \
                str(Fraction(exif_dict["ExposureTime"]["processed"]).limit_denominator(8000))

            exif_dict["ExposureBiasValue"]["processed"] = \
                self._derationalize(exif_dict["ExposureBiasValue"]["raw"])
            exif_dict["ExposureBiasValue"]["processed"] = \
                "{} EV".format(exif_dict["ExposureBiasValue"]["processed"])
        except Exception as e:
            print("Exception occured when processing EXIF Information.\n{0}".format(e))

        return exif_dict
    
    def _get_exif_info(self, imgfile):
        from PIL import Image

        try:
            image = Image.open(imgfile)
            exif = image._getexif()

            exif_data = {}

            for k, v in PIL.ExifTags.TAGS.items():
                if k in exif:
                    value = exif[k]
                else:
                    value = None

                if len(str(value)) > 64:
                    value = str(value)[:65] + "..."
                
                exif_data[v] = {"tag": k,
                    "raw": value,
                    "processed": value
                    }

            image.close()

            exif_data = self._process_exif_dict(exif_data)

            print("exif_data, type: {0}, value \n{1}".format(type(exif_data),exif_data))

            return exif_data
        except IOError as ioe:
            print("Exception parsing image information.\n{0}".format(ioe))
            return None

    def get_context_data(self, **kwargs):
        context = super(ViewImage, self).get_context_data(**kwargs)
        print("\n\n\t*** inside ViewImage.get_context_data")

        exif_info = self._get_exif_info(self.object.image_file)

        context.update({
            #'uploaded_files':files,
            'exif_info': exif_info,
        })

        return context