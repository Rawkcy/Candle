#!/usr/bin/env python

"""
available data for each trial (via NCI API)

[u'other_ids', u'record_verification_date', u'ccr_id', u'study_model_code', u'primary_purpose', u'interventional_model', u'arms', u'phase', u'completion_date', u'nci_id', u'lead_org', u'amendment_date', u'keywords', u'nct_id', u'outcome_measures', u'anatomic_sites', u'study_model_other_text', u'detail_description', u'bio_specimen', u'sites', u'eligibility', u'masking', u'number_of_arms', u'start_date', u'classification_code', u'study_subtype_code', u'diseases', u'acronym', u'current_trial_status_date', u'biomarkers', u'associated_studies', u'study_population_description', u'start_date_type_code', u'central_contact', u'collaborators', u'protocol_id', u'principal_investigator', u'ctep_id', u'current_trial_status', u'accepts_healthy_volunteers_indicator', u'dcp_id', u'official_title', u'minimum_target_accrual_number', u'brief_title', u'study_protocol_type', u'brief_summary', u'completion_date_type_code', u'sampling_method_code']
"""



import json
import urllib2
import pprint

def main(): 
    disease = 'Metastatic Breast Cancer'
    query_size = 10

    print_to_file(disease, populate_candle_trials(disease, query_size))

def populate_candle_trials(disease, query_size):
    """
    Download trials using NCI API
    Translate into Candle format
    """

    url = "https://clinicaltrialsapi.cancer.gov/v1/clinical-trials?"
    url += 'size=' + str(query_size)
    url += '&_fulltext=' + ('%20').join(disease.split(' '))

    # trials.keys() are 'total' and 'trials'
    nci_trials = json.loads(urllib2.urlopen(url).read())['trials']

    candle_trials = []
    for trial in nci_trials:
        curr_trial_info = {}

        curr_trial_info['title'] = trial['brief_title']
        curr_trial_info['nct_id'] = trial['nct_id']
        curr_trial_info['nci_id'] = trial['nci_id']
        curr_trial_info['structured_criteria'] = trial['eligibility']['structured']

        inclusion_criteria = []
        exclusion_criteria = []
        for unstructured_criteria in trial['eligibility']['unstructured']:
            if unstructured_criteria['inclusion_indicator']:
                inclusion_criteria.append(unstructured_criteria['description'])
            else:
                exclusion_criteria.append(unstructured_criteria['description'])

            curr_trial_info['inclusion_criteria'] = inclusion_criteria
            curr_trial_info['exclusion_criteria'] = exclusion_criteria

        candle_trials.append(curr_trial_info)
    return candle_trials


def print_to_file(disease, candle_trials):
    """
    Pretty print Candle trials
    """

    with open('%s.txt' % disease, 'wt') as out:
        for candle_trial in candle_trials:
            out.write("Title: %s\n" % candle_trial['title'])
            out.write("NCI ID: %s\n" % candle_trial['nci_id'])
            out.write("NCT ID: %s\n" % candle_trial['nct_id'])

            structured_criteria_text= ""
            for key, val in candle_trial['structured_criteria'].iteritems():
                structured_criteria_text += "\t%s: %s\n" %(key, val)
            out.write("Structured Criteria: \n%s\n" % structured_criteria_text)

            out.write("Inclusion Criteria: \n")
            for inclusion_criteria in candle_trial['inclusion_criteria']:
                #import ipdb;ipdb.set_trace()
                out.write("\t%s\n" % inclusion_criteria.encode('utf-8'))

            """
            out.write("Exclusion Criteria: \n")
            for exclusion_criteria in candle_trial['exclusion_criteria']:
                out.write("\t%s\n" % exclusion_criteria)
            """

            out.write("\n\n")

def usage():

    print ' -------------------------------------------------------------------------'
    print ' Roxanne Guo (roxanne.guo@me.com) '
    print ' '
    print ' Print I/E criteria for clinical trial disease type.'
    print ' '
    print ' --using NCI API '
    print ' -------------------------------------------------------------------------'
    sys.exit(' ')

if __name__ == "__main__":
    main()

