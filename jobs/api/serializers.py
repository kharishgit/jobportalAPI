from rest_framework import serializers
from jobs.models import jobs,CandidatesApplied


class jobSerializer(serializers.ModelSerializer):
    class Meta:
        model = jobs
        fields = '__all__'
        # depth = 1

class CandidatesAppliedSerializer(serializers.ModelSerializer):
    # job = jobSerializer
    job = serializers.CharField(source="jobs.title",read_only=True)
    company = serializers.CharField(source="jobs.company",read_only=True)

    class Meta:
        model = CandidatesApplied
        fields = ('user','resume','appliedAt','jobs','job','company')
        # fields = "__all__"
        # depth = 1
