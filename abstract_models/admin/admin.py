from django.contrib import admin


class AddonFieldsetsModelAdmin(admin.ModelAdmin):
    """
    Merge fieldsets from multiple admin classes

    Strongly recommended to explicitly define fields or fieldsets on the child class, since without it there is a chance
    of seeing duplicate fields
    """
    addon_fieldsets = ()

    @staticmethod
    def _fs_to_manifest(fieldsets):
        return {k: v for k, v in fieldsets}

    @staticmethod
    def _manifest_to_fs(manifest):
        return [(k, v) for k, v in manifest.items()]

    @staticmethod
    def _merge_fieldset_values(old_vals, encountered_vals):
        return {
            **old_vals,
            **encountered_vals,
            'fields': [*old_vals['fields'], *encountered_vals['fields']]
        }

    @staticmethod
    def _process_fs_manifest(fs_manifest, encountered_fs):
        for k, encountered_vals in encountered_fs:
            old_vals = fs_manifest.get(k)
            if old_vals is None:
                fs_manifest[k] = encountered_vals
            else:
                fs_manifest[k] = AddonFieldsetsModelAdmin._merge_fieldset_values(old_vals, encountered_vals)

    def get_fieldsets(self, request, obj=None):
        fs_manifest = self._fs_to_manifest(
            super(AddonFieldsetsModelAdmin, self).get_fieldsets(request, obj)
        )

        for encountered_fs in self.addon_fieldsets:
            self._process_fs_manifest(fs_manifest, encountered_fs)

        return self._manifest_to_fs(fs_manifest)
